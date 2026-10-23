"""VVA1 compare every unit before exact-once common-scale contraction."""
from data import *
def aggregate(measure,units,gs,average,group=False):
    g2=mp.mpf(gs);ls=list(map(q,measure['mass_coefficients']));total=[mp.mpf(0)]*3;slope=total[:];pole=total[:];direct=total[:]
    parts={k:total[:] for k in ['physical','Gold','soft','light']};changes={k:total[:] for k in ['wrong_roles','averaged_charges','omit_neutral','wrong_reference','missing_soft_kinetic','missing_light_kinetic']};groups={}
    for row in measure['rows']:
        if row['F2_exact_zero']:continue
        typ,key,flip,lm=work(row,g2,ls);U=units[typ][key];fv=list(map(q,U['finite']));sv=list(map(q,U['scale']));pv=list(map(q,U['pole']));W=[[mp.mpf(v) for v in line] for line in row['weights']]
        pref=mp.mpf(3)/(2*lm);j0=-mp.log(g2)+mp.log(60/lm)
        if group:
            gkey=(typ,key,str(lm))
            if gkey not in groups:groups[gkey]=[[[] for _ in range(3)] for _ in range(3)]
            for i in range(3):
                ww=[W[i][1],W[i][0],W[i][2]] if flip else W[i]
                for a in range(3):groups[gkey][i][a].append(pref*ww[a])
            continue
        ff=[fv[1],fv[0],fv[2]] if flip else fv;ss=[sv[1],sv[0],sv[2]] if flip else sv;pp=[pv[1],pv[0],pv[2]] if flip else pv
        for i in range(3):
            val=pref*mp.fsum(W[i][a]*(ff[a]+j0*ss[a]) for a in range(3));sl=pref*mp.fsum(W[i][a]*ss[a] for a in range(3))
            total[i]+=val;slope[i]+=sl;pole[i]+=pref*mp.fsum(W[i][a]*pp[a] for a in range(3));direct[i]+=pref*mp.fsum(W[i][a]*(ff[a]+(j0+mp.mpf(2)/7)*ss[a]) for a in range(3))
            parts['light' if typ=='light' else 'soft' if typ=='soft' else 'physical' if row['scalar_type']==0 else 'Gold'][i]+=val
            changes['wrong_roles'][i]+=pref*mp.fsum(W[i][a]*(fv[a]+j0*sv[a]-ff[a]-j0*ss[a]) for a in range(3))
            wrong=[mp.mpf(row['raw_weight'])*average[row['first']][i],mp.mpf(row['raw_weight'])*average[row['second']][i],W[i][2]]
            changes['averaged_charges'][i]+=pref*mp.fsum((wrong[a]-W[i][a])*(ff[a]+j0*ss[a]) for a in range(3))
            if row['neutral_scalar']:changes['omit_neutral'][i]-=val
            changes['wrong_reference'][i]-=j0*sl
            if typ=='soft':changes['missing_soft_kinetic'][i]+=pref*W[i][2]*(-2*mp.mpf(U['K'])/3)
            if typ=='light':changes['missing_light_kinetic'][i]+=pref*W[i][1 if flip else 0]*mp.mpf(5)/9
    if group:
        for (typ,key,lmtext),terms in groups.items():
            U=units[typ][key];lm=mp.mpf(lmtext);j0=-mp.log(g2)+mp.log(60/lm);fv,sv,pv=[list(map(q,U[n])) for n in ['finite','scale','pole']]
            for i in range(3):
                W=[mp.fsum(v) for v in terms[i]]
                total[i]+=mp.fsum(W[a]*(fv[a]+j0*sv[a]) for a in range(3));slope[i]+=mp.fsum(W[a]*sv[a] for a in range(3));pole[i]+=mp.fsum(W[a]*pv[a] for a in range(3));direct[i]+=mp.fsum(W[a]*(fv[a]+(j0+mp.mpf(2)/7)*sv[a]) for a in range(3))
    return {'finite_L0':total,'L_coefficient':slope,'pole':pole,'direct_L2over7':direct,'parts':parts,'changes':changes}
def main():
    start=begin('finalization_preparation.json');mp.mp.dps=110;M=packed(HERE/'combined_measure_tables.json.gz');A=packed(HERE/'primary_units_tables.json.gz');B=packed(HERE/'replay_units_tables.json.gz');maxunit=mp.mpf(0);maxquad=mp.mpf(0)
    for typ in ['positive','soft','light']:
        wanted=set().union(*(set(v[typ]) for v in M['workload'].values()));assert set(A[typ])==set(B[typ])==wanted
        for key in wanted:
            a,b=A[typ][key],B[typ][key];assert a['pole']==b['pole'] and a['scale']==b['scale']
            for v,z in zip(a['finite'],b['finite']):
                er=abs(mp.mpf(v)-mp.mpf(z))/(1+abs(mp.mpf(v)));maxunit=max(maxunit,er);assert er<mp.mpf('1e-40')
            if typ=='positive':
                h=b['histories'];assert [v['maxdegree'] for v in h]==[8,10] and max(mp.mpf(v['spin_quad_error_estimate']) for v in h)<mp.mpf('1e-50')
                er=max(abs(mp.mpf(v)-mp.mpf(z))/(1+abs(mp.mpf(z))) for v,z in zip(h[0]['finite'],h[1]['finite']));maxquad=max(maxquad,er);assert er<mp.mpf('1e-45')
    # Verify all captures/hashes before any dependent assembly.
    runs=[]
    for label,phase in [('combined','exact'),('primary','units'),('replay','units')]:
        c=json.loads((HERE/f'{label}_{phase}_capture.json').read_bytes());r=json.loads((HERE/f'{label}_{phase}_result.json').read_bytes());blob=(HERE/f'{r["role"]}_{r["kind"]}_tables.json.gz').read_bytes()
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified'] and sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
        peak=max(v['private_bytes'] for v in c['all_resource_samples']);assert peak<=8*1024**3 and c['launch']['memory']['available_pagefile']>=350*1024**2 and r['elapsed_after_imports']<600;runs.append({'label':label,'phase':phase,'seconds':r['elapsed_after_imports'],'sampled_private_max':peak})
    frame,fci,tab,ops,cas,blocks=inputs('primary');root=root_value('primary');ls=[s.S.Zero,*map(s.Rational,fci['vector_mass_eigenvalues'])];pp={(p['first_vector'],p['second_vector'],p['scalar_type']):p for p in tab['probes']}
    S0=[s.S.Zero]*3;S2=[mp.mpf(0)]*3;pole=[s.S.Zero]*3;Hp=[];reserr=mp.mpf(0)
    for b in blocks:
        H=numeric(b['H'],root);P=numeric(b['projectors'][0],root);R=(H+mp.eye(H.rows)-P)**-1*P;er=norm(H*R-P)/(1+norm(P));reserr=max(reserr,er);assert er<mp.mpf('1e-80');Hp.append(R)
    for r in range(1,5):
        for t in range(1,5):
            for i in range(3):
                S0[i]+=5*sum((b['dimension']*(s.trace(mm[1+i])/ls[r]+s.trace(mm[4+i])/ls[t]) for b,mm in zip(blocks,ops[r,t])),s.S.Zero)
                S0[i]-=sum((parse(pp[r,t,k]['qscalar_squared'][i])/ls[k-1] for k in range(2,6)),s.S.Zero)
                S2[i]-=sum((b['dimension']*real(number(cas[a][i],root))*real(tr(numeric(mm[0],root)*Hp[a])) for a,(b,mm) in enumerate(zip(blocks,ops[r,t]))),mp.mpf(0))
    for r in range(5):
        for t in range(5):
            if (r==0)==(t==0):continue
            for typ in range(2,6):
                p=pp[r,t,typ];lm=ls[max(r,t)]
                for i in range(3):
                    w1,w2,ws=[parse(p[k][i]) for k in ['q1_squared','q2_squared','qscalar_squared']]
                    S0[i]+=((-2 if r==0 else -1)*w1+(-2 if t==0 else -1)*w2+5*ws)/lm
                    pole[i]+=((-1 if r==0 else -3)*w1+(-1 if t==0 else -3)*w2+3*ws)/lm
                    assert red((w2 if r==0 else w1)-ws)==0
    S0=list(map(red,S0));pole=list(map(red,pole));cv=[12*parse(v) for v in tab['mass_sector_averaged_Casimir'][0]]
    independent=[red(-2*v*(8-v)) for v in cv];assert pole==independent==[0,-24,-30]
    average=[[real(number(parse(v),root)) for v in row] for row in tab['mass_sector_averaged_Casimir']];cases={};amperr=mp.mpf(0);scaleerr=mp.mpf(0)
    for gs in ['0.5','1.0']:
        aa=aggregate(M['measures']['primary'],A,gs,average);bb=aggregate(M['measures']['replay'],B,gs,average,True)
        for key in ['finite_L0','L_coefficient','pole','direct_L2over7']:
            for v,z in zip(aa[key],bb[key]):
                er=abs(v-z)/(1+abs(v));amperr=max(amperr,er);assert er<mp.mpf('1e-35')
        for i in range(3):
            target=real(number(S0[i],root))+mp.mpf(gs)*S2[i];er=abs(aa['L_coefficient'][i]-target)/(1+abs(target));scaleerr=max(scaleerr,er);assert er<mp.mpf('1e-55')
            assert abs(aa['pole'][i]-int(pole[i]))<mp.mpf('1e-65')
            assert abs(aa['direct_L2over7'][i]-aa['finite_L0'][i]-mp.mpf(2)/7*aa['L_coefficient'][i])<mp.mpf('1e-65')*(1+abs(aa['finite_L0'][i]))
            assert abs(sum(aa['parts'][k][i] for k in aa['parts'])-aa['finite_L0'][i])<mp.mpf('1e-65')*(1+abs(aa['finite_L0'][i]))
        assert max(abs(v) for v in aa['changes']['missing_soft_kinetic'])>mp.mpf('1e-12') and max(abs(v) for v in aa['changes']['missing_light_kinetic'])>mp.mpf('1e-3')
        cases[gs]={k:[mp.nstr(v,60) for v in aa[k]] for k in ['finite_L0','L_coefficient','pole']};cases[gs]['parts']={k:[mp.nstr(v,55) for v in vv] for k,vv in aa['parts'].items()};cases[gs]['controls']={k:[mp.nstr(v,50) for v in vv] for k,vv in aa['changes'].items()}
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<6*1024**2
    out={'schema':'VVA1_VALIDATION','status':'QUALIFIED_COMPLETE_COMMON_SCALE_VVS_PRIMITIVE','execution_state':'COMPLETED','scalar_dimension':328,'classes':35,'raw_profiles':30,'F2_profiles':29,
      'spectral_rows':M['rows'],'workload':M['workload'],'all_actual_units_compared':True,'max_unit_error':mp.nstr(maxunit,35),'max_quad_refinement':mp.nstr(maxquad,35),
      'max_common_scale_amplitude_error':mp.nstr(amperr,35),'max_direct_resolvent_scale_error':mp.nstr(scaleerr,35),'max_physical_resolvent_error':mp.nstr(reserr,35),
      'S0':list(map(str,S0)),'S2':[mp.nstr(v,65) for v in S2],'cases':cases,'remaining_overall_poles':list(map(str,pole)),
      'normalization':'Lambda_VVS=g10^2*(C(g10^2)+L*S(g10^2)+P/eps);L=log(Q2/60)',
      'proper_forest_and_actual_soft_matching_included':True,'full_parent_minus_family_included':False,'overall_counterterm_adopted':False,
      'full_positive_g_spectral_function_defined':True,'uniform_all_g_numeric_accuracy_proved':False,'full_C1_or_E5_qualified':False,
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED','native_runs':runs,
      'shared_limits':['action','reference','qualified spectral transport and scalar unit reuse','master convention','software','AI authorship'],
      'elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'validation_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'receipt_filename':'validation_receipt.json','receipt_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':out['elapsed_after_imports']},sort_keys=True),flush=True)
if __name__=='__main__':main()
