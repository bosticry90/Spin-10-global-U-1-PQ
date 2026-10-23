"""V3A1 complete coverage, distinct derivative routes and original ownership."""
from data import *
def main():
    start=begin('validation_preparation.json');mp.mp.dps=160;A,B=[packed(HERE/f'{r}_tables.json.gz') for r in ['primary','replay']]
    expected={'zero':103,'positive':12,'one_light':9,'all_light':1};assert A['counts']==B['counts']==expected
    ma,ra,sa=source('primary');mb,rb,sb=source('replay');assert ma==mb and ra==rb and len(ra)==125
    assert {tuple(r['roles']) for r in ra}=={(a,b,c) for a in range(5) for b in range(5) for c in range(5)}
    assert len(A['units'])==3 and len(B['units'])==12 and len(A['homogeneity_errors'])==len(B['homogeneity_errors'])==3
    uniterr=mp.mpf(0);permerr=mp.mpf(0);profileerr=mp.mpf(0);totalerr=mp.mpf(0)
    for key,u in A['units'].items():
        v=B['units'][key]
        for field in ['masses','scale_J','scale_J2','pole2','pole1','pole1_J']:assert all(clean(expr(a)-expr(b))==0 for a,b in zip(u[field],v[field]))
        uniterr=max(uniterr,max(abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b))) for a,b in zip(u['finite'],v['finite'])))
    for key,u in B['units'].items():
        roles=list(map(int,key.split(',')));ck,order=canonical(roles);v=B['units'][ck];inverse=[order.index(k) for k in range(3)]
        permerr=max(permerr,max(abs(mp.mpf(u['finite'][i])-mp.mpf(v['finite'][inverse[i]]))/(1+abs(mp.mpf(u['finite'][i]))) for i in range(3)))
    assert uniterr<mp.mpf('1e-70') and permerr<mp.mpf('1e-70')
    fields=['scale_J','scale_J2','pole2','pole1','pole1_J','all_light_EFT_pole2','all_light_EFT_pole1','mixed_soft_pole1_J_polynomial','forest_full_prefactor_H','forest_soft_prefactor_H','forest_hard_before_limit','forest_hard_limit']
    for field in fields:assert all(clean(expr(a)-expr(b))==0 for a,b in zip(A[field],B[field])),field
    for a,b in zip(A['profiles'],B['profiles']):
        assert a['roles']==b['roles'] and a['kind']==b['kind']
        for field in ['scale_J','scale_J2','pole2','pole1','pole1_J']:assert all(clean(expr(v)-expr(w))==0 for v,w in zip(a[field],b[field]))
        profileerr=max(profileerr,max(abs(mp.mpf(v)-mp.mpf(w))/(1+abs(mp.mpf(w))) for v,w in zip(a['finite'],b['finite'])))
    for a,b in zip(A['finite_F0'],B['finite_F0']):totalerr=max(totalerr,abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b))))
    assert profileerr<mp.mpf('1e-65') and totalerr<mp.mpf('1e-65')
    assert A['working_digits']==130 and B['working_digits']==160 and A['Kallen_fallbacks']==B['Kallen_fallbacks']==0
    hom=max(mp.mpf(v) for tab in [A,B] for v in tab['homogeneity_errors'].values());assert hom<mp.mpf('1e-70')
    leak=max(mp.mpf(v['max_imaginary_leak']) for v in [A,B]);assert leak<mp.mpf('1e-90')
    for f,sf,h in zip(A['forest_full_prefactor_H'],A['forest_soft_prefactor_H'],A['forest_hard_before_limit']):assert clean(expr(f)-expr(sf)-expr(h))==0 and not expr(h).has(Hs[0])
    whole=[[sum(weights(row)[i][k] for row in ra) for k in range(3)] for i in range(3)];assert whole==[[64]*3]*3
    p2=[clean(expr(v)+expr(w)) for v,w in zip(A['pole2'],A['all_light_EFT_pole2'])]
    p1=[clean(expr(a)+J*expr(b)+expr(c)+expr(e)) for a,b,c,e in zip(A['pole1'],A['pole1_J'],A['mixed_soft_pole1_J_polynomial'],A['all_light_EFT_pole1'])]
    assert p2==[-1152]*3 and p1==[976]*3
    assert sa['H_brackets_closed'] and sb['H_brackets_closed'] and sa['light_EFT_norm']==sb['light_EFT_norm'] and sa['light_EFT_tensor']==sb['light_EFT_tensor']
    # Actual measured-amplitude mutation controls; no chosen repair coefficients.
    avg=[mp.mpf(0)]*3;light=[mp.mpf(0)]*3;gamma=[mp.mpf(0)]*3
    for row,record in zip(ra,A['profiles']):
        typ=kind(row)
        if typ not in ['positive','one_light']:continue
        roles=row['roles'];ww=weights(row)
        if typ=='positive':
            key,order=canonical(roles);u=A['units'][key];ff=[mp.mpf(u['finite'][order.index(i)]) for i in range(3)]
        else:
            ff=hard_light(roles,ma)[0];light=[v+mp.mpf(w) for v,w in zip(light,record['finite'])]
            for i,ws in enumerate(ww):gamma[i]+=sum(q(w)*mp.pi**2 for k,w in enumerate(ws) if roles[k]!=0)
        for i in range(3):avg[i]+=sum(q(expr(row['norm'])*expr(sa['sector_averaged_Cv'][slot][i])/2)*v for slot,v in zip(roles,ff))
    base=list(map(mp.mpf,A['finite_F0']));avdiff=[v-w for v,w in zip(avg,base)]
    assert any(abs(v)>mp.mpf('1e-20') for v in avdiff) and any(abs(v)>mp.mpf('1e-20') for v in light) and any(abs(v)>mp.mpf('1e-20') for v in gamma)
    duplicate=next(v for v in A['profiles'] if v['kind']=='positive' and any(mp.mpf(x)!=0 for x in v['finite']))
    scale_loss=[num(expr(a))*mp.log(60)+num(expr(b))*mp.log(60)**2 for a,b in zip(A['scale_J'],A['scale_J2'])];assert any(v!=0 for v in scale_loss)
    forest_loss=[clean(-expr(v)) for v in A['forest_soft_prefactor_H']];assert any(v!=0 for v in forest_loss)
    controls={'omit_one_light_finite_change':list(map(lambda v:mp.nstr(-v,60),light)),
      'restore_historical_missing_gamma_finite_change':list(map(lambda v:mp.nstr(v,60),gamma)),
      'averaged_sector_charges_finite_change':list(map(lambda v:mp.nstr(v,60),avdiff)),
      'triple_full_real_cut_finite_change':list(map(lambda v:mp.nstr(2*v,60),base)),
      'duplicate_profile_roles':duplicate['roles'],'duplicate_profile_finite_change':duplicate['finite'],
      'lose_quadratic_scale_coefficients':A['scale_J2'],'wrong_common_reference_scale_finite_change':list(map(lambda v:mp.nstr(-v,60),scale_loss)),
      'drop_soft_cancelled_full_forest_change':list(map(str,forest_loss))}
    for a,b in zip(A['diagnostics'],B['diagnostics']):
        assert a['g10_squared']==b['g10_squared'] and a['L']==b['L'] and a['pole1_inside_g10_squared']==b['pole1_inside_g10_squared']
        assert max(abs(mp.mpf(v)-mp.mpf(w))/(1+abs(mp.mpf(w))) for v,w in zip(a['finite_inside_g10_squared'],b['finite_inside_g10_squared']))<mp.mpf('1e-65')
    mandatory='019db039094fadc591f6841c715beb9816f32a0f225ce2356eff0c8d064bb509';assert A['mandatory_hard_forest_correction_sha256']==B['mandatory_hard_forest_correction_sha256']==mandatory
    native=[]
    for role in ['primary','replay']:
        c=json.loads((HERE/f'{role}_capture.json').read_bytes());r=json.loads((HERE/f'{role}_result.json').read_bytes());blob=(HERE/f'{role}_tables.json.gz').read_bytes()
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
        assert sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
        peak=max(v['private_bytes'] for v in c['all_resource_samples']);assert peak<=8*1024**3 and c['launch']['memory']['available_pagefile']>=350*1024**2 and r['elapsed_after_imports']<600
        native.append({'role':role,'seconds':r['elapsed_after_imports'],'sampled_private_max':peak})
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<6*1024**2
    out={'schema':'V3A1_VALIDATION','status':'QUALIFIED_COMPLETE_THREE_VECTOR_MATCHED_PRIMITIVE_WITH_ORIGINAL_FORESTS','execution_state':'COMPLETED',
      'counts':expected,'canonical_heavy_keys':3,'ordered_heavy_keys':12,'profiles_compared':125,
      **{field:A[field] for field in ['finite_F0','scale_J','scale_J2','pole2','pole1','pole1_J','all_light_EFT_pole2','all_light_EFT_pole1','mixed_soft_pole1_J_polynomial','diagnostics']},
      'complete_adjoint_double_pole_including_EFT':list(map(str,p2)),'complete_adjoint_simple_pole_including_soft_and_EFT':list(map(str,p1)),
      'max_scaled_unit_error':mp.nstr(uniterr,45),'max_permutation_error':mp.nstr(permerr,45),'max_profile_error':mp.nstr(profileerr,45),'max_assembled_error':mp.nstr(totalerr,45),
      'max_homogeneity_error':mp.nstr(hom,45),'max_imaginary_leak':mp.nstr(leak,45),'mandatory_hard_forest_correction_sha256':mandatory,
      'original_full_family_and_soft_forests_retained':True,'remaining_overall_poles_subtracted':False,'controls':controls,'native_runs':native,
      'qualified_primitive_amplitude_inventory':7,'full_C1_or_E5_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'shared_limits':['action and reference','qualified universal kernels and soft matching','absolute dilog master','symbolic/special-function software','AI authorship'],
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
if __name__=='__main__':main()
