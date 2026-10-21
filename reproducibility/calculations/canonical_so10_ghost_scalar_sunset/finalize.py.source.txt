"""GSA1 whole-workload comparison,common-scale assembly and scale resolvent."""
from data import *
def evidence(label,phase):
    c=json.loads((HERE/f'{label}_{phase}_capture.json').read_bytes());r=json.loads((HERE/f'{label}_{phase}_result.json').read_bytes())
    assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
    peak=max(v['private_bytes'] for v in c['all_resource_samples']);assert peak<=8*1024**3 and c['launch']['memory']['available_pagefile']>=350*1024**2
    assert r['elapsed_after_imports']<600
    return {'label':label,'phase':phase,'seconds':r['elapsed_after_imports'],'sampled_private_max':peak}
def aggregate(measure,units,gs,average,grouped=False):
    g2=mp.mpf(gs);lams=list(map(q,measure['ghost_mass_coefficients']));total=[mp.mpf(0)]*3;slope=total[:];atL=total[:]
    parts={k:total[:] for k in ['physical','Gold','soft']};changes={k:total[:] for k in ['wrong_mass_roles','averaged_ghost_Casimir','missing_soft_kinetic','omitted_neutral','blind_own_reference']}
    groups={}
    for row in measure['rows']:
        if row['F2_exact_zero']:continue
        key,flip,lm=work_key(row,g2,lams);U=units['soft' if row['scalar_type']==1 else 'positive'][key]
        finite=list(map(mp.mpf,U['finite']));sc=list(map(mp.mpf,U['scale']));j0=-mp.log(g2)+mp.log(60/lm);pref=-3/lm
        weights=[[mp.mpf(v) for v in line] for line in row['weights']]
        if grouped:
            # Independent canonical-charge grouping; no reordered unit arrays.
            gkey=(key,str(lm),row['scalar_type']==1)
            if gkey not in groups:groups[gkey]=[[[] for _ in range(3)] for _ in range(3)]
            for i in range(3):
                canonical=[weights[i][1],weights[i][0],weights[i][2]] if flip else weights[i]
                for a in range(3):groups[gkey][i][a].append(pref*canonical[a])
            continue
        correct=[finite[1],finite[0],finite[2]] if flip else finite
        scales=[sc[1],sc[0],sc[2]] if flip else sc
        for i in range(3):
            fv=pref*sum(weights[i][a]*(correct[a]+j0*scales[a]) for a in range(3))
            sl=pref*sum(weights[i][a]*scales[a] for a in range(3))
            direct=pref*sum(weights[i][a]*(correct[a]+(j0+mp.mpf(2)/7)*scales[a]) for a in range(3))
            total[i]+=fv;slope[i]+=sl;atL[i]+=direct
            kind='soft' if row['scalar_type']==1 else 'Gold' if row['scalar_type']>=2 else 'physical';parts[kind][i]+=fv
            changes['wrong_mass_roles'][i]+=pref*sum(weights[i][a]*(finite[a]+j0*sc[a]-correct[a]-j0*scales[a]) for a in range(3))
            wrong=[mp.mpf(row['raw_weight'])*average[row['ghost_first']][i],mp.mpf(row['raw_weight'])*average[row['ghost_second']][i],weights[i][2]]
            changes['averaged_ghost_Casimir'][i]+=pref*sum((wrong[a]-weights[i][a])*(correct[a]+j0*scales[a]) for a in range(3))
            if row['scalar_type']==1:changes['missing_soft_kinetic'][i]+=pref*weights[i][2]*(-mp.mpf(U['kinetic_K'])/6)
            if row['neutral_scalar']:changes['omitted_neutral'][i]-=fv
            changes['blind_own_reference'][i]-=j0*sl
    if grouped:
        for (key,lmtext,issoft),W in groups.items():
            U=units['soft' if issoft else 'positive'][key];lm=mp.mpf(lmtext);j0=-mp.log(g2)+mp.log(60/lm)
            f=list(map(mp.mpf,U['finite']));sc=list(map(mp.mpf,U['scale']))
            for i in range(3):
                weights=[mp.fsum(a) for a in W[i]]
                total[i]+=mp.fsum(weights[a]*(f[a]+j0*sc[a]) for a in range(3))
                slope[i]+=mp.fsum(weights[a]*sc[a] for a in range(3))
                atL[i]+=mp.fsum(weights[a]*(f[a]+(j0+mp.mpf(2)/7)*sc[a]) for a in range(3))
    return {'finite_L0':total,'L_coefficient':slope,'direct_L_2_over7':atL,'finite_parts':parts,'changes':changes}
def main():
    start=begin('finalization_preparation.json',600);mp.mp.dps=110
    receipt=json.loads((HERE/'measure_receipt.json').read_bytes());assert receipt['status']=='QUALIFIED_COMPLETE_GHOST_SCALAR_SPECTRAL_MEASURE'
    mr={role:packed(HERE/f'{role}_measure_tables.json.gz') for role in ['primary','replay']}
    un={role:packed(HERE/f'{role}_units_tables.json.gz') for role in ['primary','replay']}
    runs=[evidence(role,'measure') for role in ['primary','replay']]+[evidence('compare','measure_comparison')]+[evidence(role,'units') for role in ['primary','replay']]
    wanted=set().union(*(set(v['positive_keys']) for v in receipt['workload'].values()));softwanted=set().union(*(set(v['soft_keys']) for v in receipt['workload'].values()))
    uniterr=mp.mpf(0);softerr=mp.mpf(0);refine=mp.mpf(0)
    for role,T in un.items():
        assert set(T['positive'])==wanted and set(T['soft'])==softwanted and T['working_digits']==110
        rr=json.loads((HERE/f'{role}_units_result.json').read_bytes());blob=(HERE/f'{role}_units_tables.json.gz').read_bytes()
        assert sha256(blob).hexdigest()==rr['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==rr['tables_sha256']
    # No dependent assembly happens until every actual positive and soft unit
    # has passed both numerical routes and its prescribed histories.
    for key in wanted:
        x,z=map(mp.mpf,key.split('|'));m=[x,mp.mpf(1),z]
        for a in range(3):
            p=un['primary']['positive'][key];r=un['replay']['positive'][key]
            u,v=mp.mpf(p['finite'][a]),mp.mpf(r['finite'][a]);delta=abs(u-v)/(1+abs(u));uniterr=max(uniterr,delta);assert delta<mp.mpf('1e-45')
            for row in [p,r]:
                assert row['pole']==['0']*3 and abs(mp.mpf(row['scale'][a])+1/(6*m[a]))<mp.mpf('1e-75')*(1+1/m[a])
            hist=r['quadrature_histories'][a];assert [q0['maxdegree'] for q0 in hist]==[8,10]
            assert max(mp.mpf(v0['error_estimate']) for v0 in hist)<mp.mpf('1e-50')
            qerr=abs(mp.mpf(hist[0]['value'])-mp.mpf(hist[1]['value']))/(1+abs(v));refine=max(refine,qerr);assert qerr<mp.mpf('1e-45')
    for key in softwanted:
        for a in range(3):
            p=un['primary']['soft'][key];r=un['replay']['soft'][key];u,v=mp.mpf(p['finite'][a]),mp.mpf(r['finite'][a])
            delta=abs(u-v)/(1+abs(u));softerr=max(softerr,delta);assert delta<mp.mpf('1e-40')
            assert p['pole']==r['pole']==['0']*3
    frame,fci,gsk,ops,cas,blocks=input_data('primary');root=root_value('primary');ls=list(map(s.Rational,fci['vector_mass_eigenvalues']))
    gt=packed(CAL/'canonical_so10_ghost_scalar_charge_kernel/primary_tables.json.gz')
    average=[[real(number(parse(v),root)) for v in row] for row in gt['mass_sector_averaged_Casimir']]
    pp={(p['first_ghost'],p['second_ghost'],p['scalar_type']):p for p in gt['probes']}
    S0=[s.S.Zero]*3;S2=[mp.mpf(0)]*3
    Hplus=[];resolvent=mp.mpf(0)
    for b in blocks:
        H=numeric(b['H'],root);P=numeric(b['projectors'][0],root);Hp=(H+mp.eye(H.rows)-P)**-1*P
        err=norm(H*Hp-P)/(1+norm(P));resolvent=max(resolvent,err);assert err<mp.mpf('1e-80');Hplus.append(Hp)
    for r in range(1,5):
        for t in range(1,5):
            for i in range(3):
                ghost=sum((s.Integer(b['dimension'])*(s.trace(M[1+i])/ls[r-1]+s.trace(M[4+i])/ls[t-1]) for b,M in zip(blocks,ops[r,t])),s.S.Zero)
                gold=sum((parse(pp[r,t,typ]['qscalar_squared'][i])/ls[typ-2] for typ in range(2,6)),s.S.Zero)
                S0[i]+=ghost/2+gold/2
                S2[i]+=sum((b['dimension']*real(number(cas[a][i],root))*real(tr(numeric(M[0],root)*Hplus[a]))/2 for a,(b,M) in enumerate(zip(blocks,ops[r,t]))),mp.mpf(0))
    S0=list(map(red,S0));s0=[real(number(v,root)) for v in S0];results={};amperr=mp.mpf(0);scaleerr=mp.mpf(0)
    for gs in ['0.5','1.0']:
        A=aggregate(mr['primary'],un['primary'],gs,average,False);B=aggregate(mr['replay'],un['replay'],gs,average,True)
        for label in ['finite_L0','L_coefficient','direct_L_2_over7']:
            for a,b in zip(A[label],B[label]):
                err=abs(a-b)/(1+abs(a));amperr=max(amperr,err);assert err<mp.mpf('1e-38')
        for i in range(3):
            prediction=s0[i]+mp.mpf(gs)*S2[i];err=abs(A['L_coefficient'][i]-prediction)/(1+abs(prediction));scaleerr=max(scaleerr,err);assert err<mp.mpf('1e-60')
            assert abs(A['direct_L_2_over7'][i]-A['finite_L0'][i]-mp.mpf(2)/7*A['L_coefficient'][i])<mp.mpf('1e-70')*(1+abs(A['finite_L0'][i]))
        assert max(abs(v) for v in A['changes']['missing_soft_kinetic'])>mp.mpf('1e-12')
        assert all(abs(sum(A['finite_parts'][kind][i] for kind in ['physical','Gold','soft'])-A['finite_L0'][i])<mp.mpf('1e-70')*(1+abs(A['finite_L0'][i])) for i in range(3))
        results[gs]={'finite_L0':[mp.nstr(v,60) for v in A['finite_L0']],'L_coefficient':[mp.nstr(v,60) for v in A['L_coefficient']],
          'direct_L_2_over7':[mp.nstr(v,60) for v in A['direct_L_2_over7']],
          'finite_parts':{k:[mp.nstr(v,55) for v in vv] for k,vv in A['finite_parts'].items()},
          'controls':{k:[mp.nstr(v,50) for v in vv] for k,vv in A['changes'].items()}}
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<6*1024**2
    out={'schema':'GSA1_VALIDATION','status':'QUALIFIED_COMPLETE_COMMON_SCALE_GHOST_SCALAR_PRIMITIVE','execution_state':'COMPLETED',
      'scalar_dimension':328,'classes':35,'spectral_rows':receipt['rows'],'raw_profiles':22,'F2_profiles':21,
      'actual_positive_unit_count':len(wanted),'actual_soft_unit_count':len(softwanted),'all_actual_units_compared':True,
      'max_positive_unit_error':mp.nstr(uniterr,30),'max_soft_unit_error':mp.nstr(softerr,30),'max_quad_refinement':mp.nstr(refine,30),
      'max_common_scale_amplitude_error':mp.nstr(amperr,30),'max_direct_resolvent_scale_error':mp.nstr(scaleerr,30),
      'max_physical_resolvent_error':mp.nstr(resolvent,30),'scale_S0':list(map(str,S0)),'scale_S2':[mp.nstr(v,65) for v in S2],
      'cases':results,'normalization':'Lambda_ghostS=g10^2*(finite_L0(g10^2)+L*L_coefficient(g10^2));L=log(Q^2/60)',
      'overall_poles':['0','0','0'],'zero_overall_pole_source':'QUALIFIED_COMPLETE_SCK1_PROPER_FOREST_IDENTITY',
      'full_positive_g_spectral_function_defined':True,'uniform_all_g_numeric_accuracy_proved':False,
      'proper_forest_and_soft_matching_included':True,'full_parent_minus_family_included':False,'overall_counterterm_adopted':False,
      'full_C1_or_E5_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'native_runs':runs,'analytic_fallbacks':un['primary']['analytic_Kallen_fallbacks'],
      'shared_limits':['action','reference xi1','scalar frame','OLD master convention','software','AI authorship'],
      'elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'validation_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'receipt_filename':'validation_receipt.json','receipt_sha256':sha256(raw).hexdigest(),
      'elapsed_after_imports':out['elapsed_after_imports']},sort_keys=True),flush=True)
if __name__=='__main__':main()
