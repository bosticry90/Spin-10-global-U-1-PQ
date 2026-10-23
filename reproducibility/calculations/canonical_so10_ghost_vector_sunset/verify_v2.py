"""GVA1 separately frozen full coverage, derivative, forest and assembly checks."""
from data_v2 import *
def main():
    start=begin('validation_v2_preparation.json');mp.mp.dps=160;A,B=[packed(HERE/f'{r}_tables.json.gz') for r in ['primary_v2','replay']]
    expected={'zero':103,'positive':12,'one_light':9,'all_light':1};assert A['counts']==B['counts']==expected
    SA,SB=[source(role) for role in ['primary','replay']];assert SA['rows']==SB['rows']
    assert len(A['profiles'])==len(B['profiles'])==125 and {tuple(v['roles']) for v in A['profiles']}=={(r,a,b) for r in range(5) for a in range(5) for b in range(5)}
    assert len(A['units'])==7 and len(B['units'])==12 and len(A['homogeneity_errors'])==len(B['homogeneity_errors'])==7
    uniterr=mp.mpf(0);exchangeerr=mp.mpf(0);assembled=mp.mpf(0);profileerr=mp.mpf(0)
    for key,u in A['units'].items():
        v=B['units'][key];assert u['scale']==v['scale'] and u['pole']==v['pole'] and u['masses']==v['masses']
        uniterr=max(uniterr,max(abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b))) for a,b in zip(u['finite'],v['finite'])))
    for key,u in B['units'].items():
        a,b,r=map(int,key.split(','));v=B['units'][f'{b},{a},{r}'];rev=[v['finite'][1],v['finite'][0],v['finite'][2]]
        exchangeerr=max(exchangeerr,max(abs(mp.mpf(c)-mp.mpf(e))/(1+abs(mp.mpf(e))) for c,e in zip(u['finite'],rev)))
    assert uniterr<mp.mpf('1e-70') and exchangeerr<mp.mpf('1e-70')
    for name in ['scale_J','remaining_pole','all_light_EFT_pole']:
        assert list(map(expr,A[name]))==list(map(expr,B[name]))
    for name in ['forest_full_prefactor_H','forest_soft_prefactor_H','forest_hard_before_limit','forest_hard_limit']:
        assert all(clean(expr(a)-expr(b))==0 for a,b in zip(A[name],B[name])),name
    for v,sf,h in zip(A['forest_full_prefactor_H'],A['forest_soft_prefactor_H'],A['forest_hard_before_limit']):assert clean(expr(v)-expr(sf)-expr(h))==0 and not expr(h).has(Hs[0])
    for a,b in zip(A['profiles'],B['profiles']):
        assert a['roles']==b['roles'] and a['kind']==b['kind'] and a['pole']==b['pole'] and a['scale']==b['scale']
        profileerr=max(profileerr,max(abs(mp.mpf(v)-mp.mpf(w))/(1+abs(mp.mpf(w))) for v,w in zip(a['finite'],b['finite'])))
    for a,b in zip(A['finite_F0'],B['finite_F0']):assembled=max(assembled,abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b))))
    assert profileerr<mp.mpf('1e-65') and assembled<mp.mpf('1e-65')
    assert A['working_digits']==130 and B['working_digits']==160 and A['Kallen_fallbacks']==B['Kallen_fallbacks']==0
    homogeneous=max(mp.mpf(v) for t in [A,B] for v in t['homogeneity_errors'].values());assert homogeneous<mp.mpf('1e-70')
    leak=max(mp.mpf(t['max_imaginary_leak']) for t in [A,B]);assert leak<mp.mpf('1e-90')
    for a,b in zip(A['diagnostics'],B['diagnostics']):
        assert a['g10_squared']==b['g10_squared'] and a['L']==b['L']
        err=max(abs(mp.mpf(v)-mp.mpf(w))/(1+abs(mp.mpf(w))) for v,w in zip(a['coefficient_inside_g10_squared'],b['coefficient_inside_g10_squared']));assert err<mp.mpf('1e-65')
    # Group marginal uses complete action-derived charge traces, not fitted poles.
    whole=[[sum(weights(row)[i][k] for row in SA['rows']) for k in range(3)] for i in range(3)]
    assert whole==[[-64]*3]*3
    combined=[clean(expr(v)+expr(w)) for v,w in zip(A['remaining_pole'],A['all_light_EFT_pole'])];assert combined==[112]*3
    # Materialized mutations on actual measured inputs and computed units.
    masses=list(map(expr,SA['mass_coefficients']));base=list(map(mp.mpf,A['finite_F0']));avg=[mp.mpf(0)]*3;wrong=[mp.mpf(0)]*3;light=[mp.mpf(0)]*3
    for row,record in zip(SA['rows'],A['profiles']):
        typ=kind(row)
        if typ in ['zero','all_light']:continue
        r,a,b=ids(row);ww=weights(row)
        if typ=='positive':
            key,swap=canonical(row);ff=list(map(mp.mpf,A['units'][key]['finite']))
            if swap:ff[0],ff[1]=ff[1],ff[0]
        else:ff,_=light_kernel(row,masses)
        if typ=='one_light':light=[v+mp.mpf(w) for v,w in zip(light,record['finite'])]
        for i in range(3):
            av=[expr(row['signed_raw'])*expr(SA['sector_averaged_Cv'][slot][i]) for slot in [a,b,r]]
            avg[i]+=sum(q(s.Rational(3,4)*w)*v for w,v in zip(av,ff))
            wrong[i]+=sum(q(s.Rational(3,4)*w)*v for w,v in zip([ww[i][1],ww[i][0],ww[i][2]],ff))
    avdiff=[v-w for v,w in zip(avg,base)];orderdiff=[v-w for v,w in zip(wrong,base)]
    assert any(abs(v)>mp.mpf('1e-20') for v in avdiff) and any(abs(v)>mp.mpf('1e-20') for v in orderdiff)
    assert any(abs(v)>mp.mpf('1e-20') for v in light) and any(abs(v)>mp.mpf('1e-20') for v in base)
    selected=next(v for v in A['profiles'] if v['kind']=='positive' and any(mp.mpf(x)!=0 for x in v['finite']))
    duplicate=list(map(mp.mpf,selected['finite']));assert any(v!=0 for v in duplicate)
    scale_wrong=[q(expr(v))*mp.log(60) for v in A['scale_J']];assert any(v!=0 for v in scale_wrong)
    forest_loss=[clean(-expr(v)) for v in A['forest_soft_prefactor_H']];assert any(v!=0 for v in forest_loss)
    controls={'ghost_sign_reversal_finite_change':[mp.nstr(-2*v,60) for v in base],
      'omit_light_profiles_finite_change':[mp.nstr(-v,60) for v in light],
      'averaged_sector_charge_finite_change':[mp.nstr(v,60) for v in avdiff],
      'wrong_ordered_ghost_charge_finite_change':[mp.nstr(v,60) for v in orderdiff],
      'duplicate_profile_roles':selected['roles'],'duplicate_profile_finite_change':list(map(lambda v:mp.nstr(v,60),duplicate)),
      'incompatible_reference_scale_change':list(map(lambda v:mp.nstr(v,60),scale_wrong)),
      'drop_soft_cancelled_full_family_forest_change':list(map(str,forest_loss))}
    native=[]
    for role in ['primary_v2','replay']:
        c=json.loads((HERE/f'{role}_capture.json').read_bytes());r=json.loads((HERE/f'{role}_result.json').read_bytes());blob=(HERE/f'{role}_tables.json.gz').read_bytes()
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
        assert sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
        peak=max(v['private_bytes'] for v in c['all_resource_samples']);assert peak<=8*1024**3 and c['launch']['memory']['available_pagefile']>=350*1024**2 and r['elapsed_after_imports']<600
        native.append({'role':role,'seconds':r['elapsed_after_imports'],'sampled_private_max':peak})
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<6*1024**2
    out={'schema':'GVA1_VALIDATION','status':'QUALIFIED_COMPLETE_GHOST_VECTOR_MATCHED_PRIMITIVE_WITH_ORIGINAL_FORESTS','execution_state':'COMPLETED',
      'counts':expected,'canonical_heavy_keys':7,'ordered_heavy_keys':12,'profiles_compared':125,'remaining_pole':A['remaining_pole'],'all_light_EFT_pole':A['all_light_EFT_pole'],
      'complete_adjoint_pole_including_EFT':list(map(str,combined)),'finite_F0':A['finite_F0'],'scale_J':A['scale_J'],'diagnostics':A['diagnostics'],
      'max_scaled_unit_error':mp.nstr(uniterr,40),'max_ghost_exchange_error':mp.nstr(exchangeerr,40),'max_profile_error':mp.nstr(profileerr,40),
      'max_assembled_error':mp.nstr(assembled,40),'max_homogeneity_error':mp.nstr(homogeneous,40),'max_imaginary_leak':mp.nstr(leak,40),
      'original_full_family_and_soft_forests_retained':True,'remaining_overall_pole_subtracted':False,'controls':controls,'native_runs':native,
      'qualified_primitive_amplitude_inventory':6,'full_C1_or_E5_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'shared_limits':['action','qualified universal kernels','absolute dilog master','regulator/matching','software','AI authorship'],
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
if __name__=='__main__':main()
