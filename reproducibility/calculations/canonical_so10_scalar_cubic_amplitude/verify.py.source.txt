"""S3A1 full SSS amplitude, complete forest and independent scale function."""
from data import *
start=begin('validation_preparation.json');mp.mp.dps=150
a=packed(HERE/'primary_tables.json.gz');b=packed(HERE/'replay_tables.json.gz')
spec=importlib.util.spec_from_file_location('s3a_validation_measure',CAL/'canonical_so10_scalar_cubic_spectral_measure/data.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
assert a['working_digits']==110 and b['working_digits']==140 and a['remaining_overall_pole']==b['remaining_overall_pole']==[0,0,0]
count,error=M.compare({k:v for k,v in a.items() if k!='working_digits'},{k:v for k,v in b.items() if k!='working_digits'},'1e-38')
source=packed(CAL/'canonical_so10_scalar_cubic_class_gram/primary_tables.json.gz');exactnorms={k:M.real(M.pnumber(v)) for k,v in source['norms'].items()}
scale_error=mp.mpf(0);forest_error=mp.mpf(0);max_domain=mp.mpf(0)
for gs,case in a['cases'].items():
    g2=q(gs);finite=list(map(q,case['finite_L0']));slope=list(map(q,case['scale_linear']));direct=list(map(q,case['direct_L_2_over7']))
    for h in range(3):
        prediction=q(a['independent_slope']['constant_A'][h])+q(a['independent_slope']['inverse_g2_B'][h])/g2
        err=abs(prediction-slope[h])/(1+abs(prediction));scale_error=max(scale_error,err);assert err<mp.mpf('1e-55')
        assert abs(direct[h]-finite[h]-mp.mpf(2)/7*slope[h])<mp.mpf('1e-55')*(1+abs(finite[h]))
        total=mp.fsum(q(v[h]) for v in case['finite_by_soft_count'].values());max_domain=max(max_domain,abs(total-finite[h])/(1+abs(finite[h])));assert max_domain<mp.mpf('1e-55')
        # Each original three-cut forest is mu*W*c/12, independent of its
        # closing mass. All source charge norms sum mu*W*(c1+c2+c3)/3.
        fc=mp.fsum(q(v[h]) for v in case['original_forest_by_closing_mass'].values());want=exactnorms[['U1','SU2','SU3'][h]]/4
        err=abs(fc-want)/(1+abs(want));forest_error=max(forest_error,err);assert err<mp.mpf('1e-55'),('THREE_CUT_FOREST_NORM',h)
    blueprint=case['full_original_forest_blueprint'];assert len(blueprint)==1602*3
    assert sum(v['original_common_delta_closing'] for v in blueprint)==234
    summed={}
    for row in blueprint:
        key=row['closing_mass_key'];acc=summed.setdefault(key,[mp.mpf(0)]*3)
        for h in range(3):acc[h]+=q(row['coefficient_of_Hm_over_m_epsilon'][h])
    for k,values in summed.items():
        for got,want in zip(values,map(q,case['original_forest_by_closing_mass'][k])):assert abs(got-want)<mp.mpf('1e-55')*(1+abs(want))
    controls=case['controls']
    for name in ['wrong_axis_permutation','delete_soft_domains','omit_soft_kinetic','blind_Q1_reference','omit_overlap_at_delta_over_M_1e-20']:
        assert max(abs(q(v)) for v in controls[name])>mp.mpf('1e-12'),('INSENSITIVE_REQUIRED_CONTROL',name)
    for u,v in zip(controls['omit_overlap_at_delta_over_M_1e-20'],controls['omit_overlap_at_delta_over_M_1e-40']):assert abs(q(v)-2*q(u))<mp.mpf('1e-55')*(1+abs(q(v)))
    if gs=='1/2':assert max(abs(q(v)) for v in controls['extra_g2_prefactor'])>mp.mpf('1e-12')
    else:assert all(q(v)==0 for v in controls['extra_g2_prefactor'])
assert a['cases']['1/2']['original_forest_by_closing_mass']==a['cases']['1']['original_forest_by_closing_mass']
assert a['cases']['1/2']['full_original_forest_blueprint']==a['cases']['1']['full_original_forest_blueprint']
receipt={'schema':'S3A1_VALIDATION','status':'QUALIFIED_COMPLETE_SCALAR_CUBIC_MATCHED_PRIMITIVE','execution_state':'COMPLETED',
 'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED','scalar_fields':328,'SM_classes':35,'mode_rows':1728,
 'required_F2_rows':1602,'canonical_mass_keys':688,'actual_unit_assignments':956,'primitive_amplitude_inventory':9,
 'diagnostics':{gs:{k:v for k,v in case.items() if k not in ['full_original_forest_blueprint','original_forest_by_closing_mass']} for gs,case in a['cases'].items()},
 'independent_scale_coefficients':a['independent_slope'],'numeric_comparisons':count,'max_scaled_amplitude_comparison':mp.nstr(error,35),
 'max_independent_resolvent_scale_error':mp.nstr(scale_error,35),'max_three_cut_forest_norm_error':mp.nstr(forest_error,35),'max_domain_sum_error':mp.nstr(max_domain,35),
 'original_three_cut_forest_entries':4806,'original_soft_closings':234,'full_original_forest_owned_by_parent_minus_family':True,
 'common_scale':'L=log(Q2/60)','scale_form':'A+B/g10^2','universal_g10_squared_prefactor':False,'remaining_overall_pole':[0,0,0],
 'SSS_amplitude_complete_within_declared_reference_scope':True,'uniform_all_g_numeric_bound':False,
 'full_parent_background_CT_matching_conversion_C1_E5_A5_or_physical_unification_qualified':False,
 'shared_error_limits':['physical action/point/cubic/frame/spectrum/Casimirs','common-delta matching/reference/subtraction/master conventions','software','AI authorship'],
 'elapsed_after_imports':time.perf_counter()-start}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
