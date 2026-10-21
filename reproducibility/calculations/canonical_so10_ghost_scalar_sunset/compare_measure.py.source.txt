"""Complete GSA1 spectral coverage and row comparison before finite units."""
from data import *
def main():
    start=begin('measure_comparison_preparation.json',600);mp.mp.dps=110
    A=packed(HERE/'primary_measure_tables.json.gz');B=packed(HERE/'replay_measure_tables.json.gz')
    def key(r):return tuple(r[k] for k in ['ghost_first','ghost_second','scalar_block','scalar_id','scalar_type'])
    aa={key(r):r for r in A['rows']};bb={key(r):r for r in B['rows']};assert len(aa)==len(A['rows']) and set(aa)==set(bb)
    assert A['counts']==B['counts']==[290,5,8,1,12,12]
    assert A['working_digits']==B['working_digits']==110 and not A['magnitude_cutoff_used'] and not B['magnitude_cutoff_used']
    error=mp.mpf(0)
    for k,row in aa.items():
        rr=bb[k]
        for f in ['F2_exact_zero','neutral_scalar','scalar_g2_power']:assert row[f]==rr[f]
        for u,v in [(row['scalar_mass_base'],rr['scalar_mass_base']),(row['raw_weight'],rr['raw_weight']),*zip(sum(row['weights'],[]),sum(rr['weights'],[]))]:
            u,v=mp.mpf(u),mp.mpf(v);error=max(error,abs(u-v)/(1+abs(u)));assert abs(u-v)<mp.mpf('1e-60')*(1+abs(u))
    frame,fci,tab,ops,cas,blocks=input_data('primary');root=root_value('primary')
    pp={(p['first_ghost'],p['second_ghost'],p['scalar_type']):p for p in tab['probes']}
    expected=set();marginal=mp.mpf(0);moment=mp.mpf(0)
    for r in range(1,5):
        for t in range(1,5):
            p=pp[r,t,0];admitted=any(parse(v)!=0 for v in [p['raw'],*p['q1_squared'],*p['q2_squared'],*p['qscalar_squared']])
            for alpha,b in enumerate(blocks):
                M0=ops[r,t][alpha]
                rank=int(red(s.trace(b['projectors'][0])))
                if admitted and any(M.todok() for M in M0):
                    for i in range(rank):expected.add((r,t,alpha,'physical_'+str(i),0))
                rows=[v for k,v in aa.items() if k[0]==r and k[1]==t and k[2]==alpha]
                N=[numeric(M,root) for M in M0];H=numeric(b['H'],root);P=numeric(b['projectors'][0],root)
                Fzero=(not M0[0].todok() or all(c==0 for c in cas[alpha])) and not any(M.todok() for M in M0[1:])
                for row in rows:
                    assert row['F2_exact_zero']==Fzero and mp.mpf(row['scalar_mass_base'])>0
                    if Fzero:assert all(mp.mpf(v)==0 for vals in row['weights'] for v in vals)
                for power in [0,1,2]:
                    for i,M in enumerate(N):
                        def value(row):
                            if i==0:return mp.mpf(row['raw_weight'])
                            return mp.mpf(row['weights'][i-1][0]) if i<=3 else mp.mpf(row['weights'][i-4][1])
                        actual=sum((mp.mpf(row['scalar_mass_base'])**power*value(row) for row in rows),mp.mpf(0))
                        target=b['dimension']*real(tr(M*(H**power)*P))
                        delta=abs(actual-target)/(1+abs(target));moment=max(moment,delta);assert delta<mp.mpf('1e-60')
            for typ in range(6):
                p=pp[r,t,typ];numbers=[p['raw'],*p['q1_squared'],*p['q2_squared'],*p['qscalar_squared']]
                if typ and any(parse(v)!=0 for v in numbers):expected.add((r,t,-1,str(typ),typ))
                rows=[v for k,v in aa.items() if k[0]==r and k[1]==t and k[4]==typ]
                targets=[real(number(parse(v),root)) for v in numbers]
                actual=[sum((mp.mpf(row['raw_weight']) for row in rows),mp.mpf(0))]
                actual += [sum((mp.mpf(row['weights'][i][axis]) for row in rows),mp.mpf(0)) for axis in range(3) for i in range(3)]
                for a,v in zip(actual,targets):
                    delta=abs(a-v)/(1+abs(v));marginal=max(marginal,delta);assert delta<mp.mpf('1e-60')
    assert set(aa)==expected
    for role,T in [('primary',A),('replay',B)]:
        lams=list(map(q,T['ghost_mass_coefficients']))
        for gs,work in T['workload'].items():
            pos={};soft={}
            for row in T['rows']:
                if row['F2_exact_zero']:continue
                u,flip,lm=work_key(row,mp.mpf(gs),lams);owner=f"{min(row['ghost_first'],row['ghost_second'])},{max(row['ghost_first'],row['ghost_second'])}"
                (soft if mp.mpf(u.split('|')[1])==0 else pos)[u]=owner
            assert dict(sorted(pos.items()))==work['positive_keys'] and dict(sorted(soft.items()))==work['soft_keys']
        c=json.loads((HERE/f'{role}_measure_capture.json').read_bytes());r=json.loads((HERE/f'{role}_measure_result.json').read_bytes())
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['post_run_observations_qualified'] and r['elapsed_after_imports']<600
        blob=(HERE/f'{role}_measure_tables.json.gz').read_bytes();assert sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
    assert A['workload']==B['workload']
    receipt={'schema':'GSA1_MEASURE_VALIDATION','status':'QUALIFIED_COMPLETE_GHOST_SCALAR_SPECTRAL_MEASURE',
      'rows':len(aa),'counts':A['counts'],'raw_profiles':len(A['raw_support_profiles']),'F2_zero_rows':A['exact_F2_zero_rows'],
      'max_role_error':mp.nstr(error,30),'max_spectral_moment_error':mp.nstr(moment,30),'max_exact_marginal_error':mp.nstr(marginal,30),
      'workload':A['workload'],'all_structurally_admitted_modes_retained':True,'finite_amplitude_qualified':False,
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED','elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(receipt,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'measure_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'receipt_filename':'measure_receipt.json','receipt_sha256':sha256(raw).hexdigest(),
      'elapsed_after_imports':receipt['elapsed_after_imports']},sort_keys=True),flush=True)
if __name__=='__main__':main()
