"""VVA1 exact transport of qualified physical spectra and new Gold/soft weights."""
from data import *
def main():
    start=begin('preparation.json');mp.mp.dps=110;measures={};workload={};comparison=mp.mpf(0)
    for role in ['primary','replay']:
        frame,fci,tab,ops,cas,blocks=inputs(role);root=root_value(role);lams=[mp.mpf(0),*map(q,fci['vector_mass_eigenvalues'])]
        old=packed(CAL/'canonical_so10_ghost_scalar_sunset'/f'{role}_measure_tables.json.gz');rows=[]
        for src in old['rows']:
            if src['scalar_type']!=0:continue
            row={k:v for k,v in src.items() if k not in ['ghost_first','ghost_second']};row['first']=src['ghost_first'];row['second']=src['ghost_second']
            row['raw_weight']=mp.nstr(4*mp.mpf(src['raw_weight']),75);row['weights']=[[mp.nstr(4*mp.mpf(v),75) for v in line] for line in src['weights']];rows.append(row)
        lookup={(p['first_vector'],p['second_vector'],p['scalar_type']):p for p in tab['probes']}
        for r in range(5):
            for t in range(5):
                for typ in range(1,6):
                    p=lookup[r,t,typ];raw=parse(p['raw']);ws=[[parse(p[k][i]) for k in ['q1_squared','q2_squared','qscalar_squared']] for i in range(3)]
                    if raw==0 and all(v==0 for line in ws for v in line):continue
                    rows.append({'first':r,'second':t,'scalar_block':-1,'scalar_id':str(typ),'scalar_type':typ,
                      'scalar_mass_base':'0.0' if typ==1 else mp.nstr(lams[typ-1],85),'scalar_g2_power':0 if typ==1 else 1,
                      'raw_weight':mp.nstr(real(number(raw,root)),75),'weights':[[mp.nstr(real(number(v,root)),75) for v in line] for line in ws],
                      'F2_exact_zero':all(v==0 for line in ws for v in line),'neutral_scalar':False})
        profiles=sorted(set((r['first'],r['second'],r['scalar_type']) for r in rows));assert profiles==list(map(tuple,sorted(json.loads((CAL/'canonical_so10_vector_vector_scalar_charge_kernel/validation_receipt.json').read_bytes())['raw_nonzero_profiles'])))
        measures[role]={'rows':rows,'mass_coefficients':['0',*fci['vector_mass_eigenvalues']],'profiles':profiles,'counts':old['counts']}
    def key(v):return tuple(v[k] for k in ['first','second','scalar_block','scalar_id','scalar_type'])
    aa={key(v):v for v in measures['primary']['rows']};bb={key(v):v for v in measures['replay']['rows']};assert set(aa)==set(bb)
    for k,A in aa.items():
        B=bb[k];assert A['F2_exact_zero']==B['F2_exact_zero'] and A['scalar_g2_power']==B['scalar_g2_power']
        for a,b in zip([A['scalar_mass_base'],A['raw_weight'],*[v for line in A['weights'] for v in line]],
          [B['scalar_mass_base'],B['raw_weight'],*[v for line in B['weights'] for v in line]]):
            err=abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(a)));comparison=max(comparison,err);assert err<mp.mpf('1e-65')
    for gs in ['0.5','1.0']:
        wanted={typ:set() for typ in ['positive','soft','light']}
        for row in aa.values():
            if row['F2_exact_zero']:continue
            typ,k,flip,lm=work(row,mp.mpf(gs),list(map(q,measures['primary']['mass_coefficients'])));wanted[typ].add(k)
        workload[gs]={typ:sorted(keys) for typ,keys in wanted.items()}
    save('combined','measure',{'schema':'VVA1_MEASURE','measures':measures,'workload':workload,'measure_comparison_error':mp.nstr(comparison,35),
      'rows':len(aa),'counts':[290,5,8,1,12,12],'source':'QUALIFIED_VVK1_PHYSICAL_TRANSPORT_AND_NEW_GOLD_SOFT_PROBES',
      'mass_digits':85,'weight_digits':75,'working_digits':110,'magnitude_cutoff_used':False,'scientific_acceptance':'NOT_PERFORMED'},start)
if __name__=='__main__':main()
