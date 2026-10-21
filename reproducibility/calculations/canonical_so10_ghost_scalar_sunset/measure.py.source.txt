"""GSA1 full physical-H spectrum plus exact degenerate Gold/soft sums."""
from data import *
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin('preparation.json',600);mp.mp.dps=110
    frame,fci,tab,operators,cas,blocks=input_data(role);root=root_value(role);lams=list(map(q,fci['vector_mass_eigenvalues']))
    modes=[modes_for_block(b,fci['vector_mass_eigenvalues'],root,role) for b in blocks]
    counts=[sum(b['dimension']*(1 if m['type']==0 else int(red(s.trace(b['projectors'][m['type']])))) for b,ms in zip(blocks,modes) for m in ms if m['type']==typ) for typ in range(6)]
    assert counts==[290,5,8,1,12,12]
    lookup={(p['first_ghost'],p['second_ghost'],p['scalar_type']):p for p in tab['probes']}
    rows=[];max_moment=mp.mpf(0);neutral_weight=mp.mpf(0);definitions=[]
    for aa,b in enumerate(blocks):
        definitions.append({'block':aa,'multiplicity':b['multiplicity'],'dimension':b['dimension'],'label':b['label'],
          'H':enc(b['H']),'projectors':list(map(enc,b['projectors'])),'Casimirs':list(map(str,cas[aa]))})
    for r in range(1,5):
        for t in range(1,5):
            physicalsums=[mp.mpf(0)]*7
            pp=lookup[r,t,0]
            admitted=any(parse(v)!=0 for v in [pp['raw'],*pp['q1_squared'],*pp['q2_squared'],*pp['qscalar_squared']])
            for aa,b in (enumerate(blocks) if admitted else []):
                exact=operators[r,t][aa]
                if not any(M.todok() for M in exact):continue
                scalar_zero=not exact[0].todok() or all(c==0 for c in cas[aa])
                Fzero=scalar_zero and not any(M.todok() for M in exact[1:])
                M=[numeric(X,root) for X in exact];cv=[real(number(c,root)) for c in cas[aa]]
                collected=[[] for _ in range(7)]
                for mode in modes[aa]:
                    if mode['type']!=0:continue
                    weight=[b['dimension']*real(tr(X*mode['P'])) for X in M]
                    physicalsums=[a+v for a,v in zip(physicalsums,weight)]
                    for k,v in enumerate(weight):collected[k].append((mode['mass_base'],v))
                    ws=[[weight[1+i],weight[4+i],weight[0]*cv[i]] for i in range(3)]
                    if Fzero:assert all(v==0 for row in ws for v in row)
                    if all(c==0 for c in cas[aa]):neutral_weight+=sum(abs(v) for row in ws for v in row)
                    rows.append({'ghost_first':r,'ghost_second':t,'scalar_block':aa,'scalar_id':mode['id'],'scalar_type':0,
                      'scalar_mass_base':mp.nstr(mode['mass_base'],85),'scalar_g2_power':0,
                      'raw_weight':mp.nstr(weight[0],75),'weights':[[mp.nstr(v,75) for v in row] for row in ws],
                      'F2_exact_zero':Fzero,'neutral_scalar':all(c==0 for c in cas[aa])})
                H=numeric(b['H'],root);P=numeric(b['projectors'][0],root)
                for power in [0,1,2]:
                    HP=(H**power)*P
                    for k in range(7):
                        target=b['dimension']*real(tr(M[k]*HP));actual=sum((mass**power*v for mass,v in collected[k]),mp.mpf(0))
                        err=abs(actual-target)/(1+abs(target));max_moment=max(max_moment,err);assert err<mp.mpf('1e-80')
            expected=[pp['raw'],*pp['q1_squared'],*pp['q2_squared']]
            for a,v in zip(physicalsums,expected):assert abs(a-real(number(parse(v),root)))<mp.mpf('1e-75')*(1+abs(a))
            for typ in range(1,6):
                p=lookup[r,t,typ];raw=parse(p['raw']);ws=[[parse(p[k][i]) for k in ['q1_squared','q2_squared','qscalar_squared']] for i in range(3)]
                if raw==0 and all(v==0 for row in ws for v in row):continue
                rows.append({'ghost_first':r,'ghost_second':t,'scalar_block':-1,'scalar_id':str(typ),'scalar_type':typ,
                  'scalar_mass_base':'0.0' if typ==1 else mp.nstr(lams[typ-2],85),'scalar_g2_power':0 if typ==1 else 1,
                  'raw_weight':mp.nstr(real(number(raw,root)),75),
                  'weights':[[mp.nstr(real(number(v,root)),75) for v in row] for row in ws],
                  'F2_exact_zero':all(v==0 for row in ws for v in row),'neutral_scalar':False})
            print('STAGE '+role+'_full_spectrum_ghost_pair_'+str(r)+','+str(t),flush=True)
    workload={};profiles={}
    for row in rows:
        key=tuple(row[k] for k in ['ghost_first','ghost_second','scalar_type']);profiles[key]=profiles.get(key,0)+1
    for gs in ['0.5','1.0']:
        keys={};soft={};g2=mp.mpf(gs)
        for row in rows:
            if row['F2_exact_zero']:continue
            key,flip,lammax=work_key(row,g2,lams);ratio,z=key.split('|')
            owner=f"{min(row['ghost_first'],row['ghost_second'])},{max(row['ghost_first'],row['ghost_second'])}"
            if mp.mpf(z)>0:keys[key]=owner
            else:soft[key]=owner
        workload[gs]={'positive_keys':dict(sorted(keys.items())),'soft_keys':dict(sorted(soft.items())),
          'positive_unit_count':len(keys),'soft_unit_count':len(soft)}
    save(role,'measure',{'schema':'GSA1_MEASURE','working_digits':110,'mass_output_digits':85,'weight_output_digits':75,
      'blocks':definitions,'counts':counts,'ghost_mass_coefficients':fci['vector_mass_eigenvalues'],
      'rows':rows,'raw_support_profiles':[[*k,n] for k,n in sorted(profiles.items())],
      'exact_F2_zero_rows':sum(v['F2_exact_zero'] for v in rows),'neutral_scalar_absolute_charge_weight':mp.nstr(neutral_weight,50),
      'max_physical_spectral_moment_error':mp.nstr(max_moment,30),'workload':workload,
      'full_Gold_soft_degenerate_weights':'EXACT_GSK_FULL_FIELD_PROBES','magnitude_cutoff_used':False,
      'finite_amplitude_qualified':False,'scientific_acceptance':'NOT_PERFORMED'},start)
if __name__=='__main__':main()
