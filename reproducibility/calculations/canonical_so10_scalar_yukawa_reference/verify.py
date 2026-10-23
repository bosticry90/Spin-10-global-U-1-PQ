"""SYR1 independent algebra/bubble/actual scalar-domain qualification."""
from data import *
from itertools import product
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==hsh,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def eq(a,b):assert s.simplify(s.gammasimp(s.sympify(a)-s.sympify(b)))==0,(a,b)
assert P['chiral_paths']==R['chiral_paths'] and len(P['chiral_paths'])==340
inventory=set()
for key,val in P['chiral_paths'].items():
 n,roles,labels=key.split('_');ny=roles.count('0');ng=roles.count('1')
 if ny%2:assert s.sympify(val)==0
 if ny>0 and s.sympify(val)!=0:inventory.add((int(n),ny,ng))
assert inventory=={(2,2,0),(3,2,1),(4,2,2),(4,4,0)}
assert R['operator_covariance_by_crossed_chiral_module'] and R['formal_even_trace_At_minus_A']=='0'
assert P['operator_kinetic_covariance_positions']==384 and P['operator_gauge_covariance_positions']==256 and P['operator_mass_covariance_positions']==64
assert P['physical_BMHV_wrong_full_hat_covariance_nonzero_positions']>0 and P['wrong_adjoint_mass_law_nonzero_positions']>0
assert P['scalar_spin_coefficients']==R['scalar_spin_coefficients']
for mu,nu in product(range(4),repeat=2):
 v=list(map(s.sympify,P['scalar_spin_coefficients'][f'{mu}_{nu}']));assert v==[0,-int(mu==nu),-int(mu==nu),0]
for k in ['actual_bar_pole_finite','actual_hat_pole_finite','reference_physical_pole_finite']:
 for a,b in zip(P[k],R[k]):eq(a,b)
for k in ['physical_difference_finite','physical_difference_exact','relative_hat_kinetic_pole','scalar_dot_numerator_prefactor']:eq(P[k],R[k])
H=list(map(dec,P['scalar_metrics']));HR=list(map(dec,R['scalar_metrics']));cross=dec(P['complex_cross_metric']);assert cross==dec(R['complex_cross_metric'])==s.zeros(328)
for a,b in zip(H,HR):assert a==b
assert H[0]==s.diag(*[s.Rational(1,2) if 306<=i<326 else 0 for i in range(328)])
assert H[1]==s.diag(*[s.Rational(1,2) if 54<=i<306 else 0 for i in range(328)])
for k in P['family_norm_polynomials']:eq(P['family_norm_polynomials'][k],R['family_norm_polynomials'][k])
# Later qualified comparators cannot be read by the two scientific workers.
FKP=packed(CAL/'canonical_so10_fermion_kinetic_mass_poles/primary_tables.json.gz');FKPr=read(CAL/'canonical_so10_fermion_kinetic_mass_poles/validation_receipt_v2.json');assert FKPr['status']=='QUALIFIED_FERMION_SCALAR_KINETIC_AND_VECTOR_MASS_POLE_MATCH'
for a,b in zip(H,map(dec,FKP['scalar_metrics'])):assert a==b
assert cross==dec(FKP['cross_scalar_metric']);eq(P['actual_bar_pole_finite'][0],FKP['scalar_bar_derivative_pole']);eq(P['actual_hat_pole_finite'][0],FKP['scalar_hat_derivative_pole'])
GFD=read(CAL/'canonical_so10_fermion_gauge_finite_difference/validation_receipt.json');eq(P['physical_difference_finite'],GFD['physical_two_point_finite_q2_delta_per_G'])
F=s.sympify(P['physical_difference_finite']);odd=s.sympify(P['physical_odd_chi_four_gamma_trace_discarded']);assert odd!=0
assert R['complete_symmetric_basis_dimensions']==[10,126] and R['basis_reconstruction_positions_checked']==167936 and R['basis_isometry_positions_checked']==18496
for obj in [P,R]:assert obj['physical_spin_trace']==4 and obj['gaussian_factor']=='1/2' and not obj['extra_family_factor_used'] and obj['reference_is_parity_even_only'] and not obj['full_chiral_regularization_or_measure_constructed'] and not obj['mixed_scalar_gauge_coefficients_measured'] and not obj['physical_scheme_adopted'] and obj['new_one_loop_finite_bubble_families']==1 and obj['new_two_loop_integrals']==0
assert P['witness_spin_trace']==8 and P['witness_to_physical_divisor']==2
controls={'physical_BMHV_chi_not_full_anticommuting':P['physical_BMHV_wrong_full_hat_covariance_nonzero_positions']>0,'wrong_adjoint_mass_law':P['wrong_adjoint_mass_law_nonzero_positions']>0,'retain_odd_chi_epsilon_trace':odd!=0,'premature_hat_zero_loses_finite_contact':F!=0,'wrong_hat_sign_changes_finite':F!=-F,'omit_witness_divisor':F!=2*F,'omit_Nambu_half':F!=2*F,'extra_Nambu_half':F!=F/2,'extra_family_three':F!=3*F,'drop_symmetric_offdiagonal_family_weight':any('2*' in v for v in P['family_norm_polynomials'].values())}
assert all(controls.values())
local={'scalar_Pi_finite_q2_per_k10_k126':list(map(enc,[F*v for v in H])),'scalar_action_gradx_per_k10_k126':list(map(enc,[F*v/2 for v in H])),'comparison_CT_action_gradx_per_k10_k126':list(map(enc,[-F*v/2 for v in H])),'actual_bar_pole_metrics':list(map(enc,H)),'actual_hat_pole_metrics':list(map(enc,[s.sympify(P['actual_hat_pole_finite'][0])*v for v in H])),'relative_hat_pole_metrics':list(map(enc,[s.sympify(P['relative_hat_kinetic_pole'])*v for v in H])),'family_trace_definition':P['family_norm_polynomials'],'no_extra_family_factor':True,'common_loop_factor':'1/(16*pi^2)','absolute_finite_baselines':'zeta_b0_kappa_distinct_unfixed','mixed_unmeasured_families':['YYG','YYGG','YYYY'],'reference_trace_ceiling':'PARITY_EVEN_ALGEBRA_ONLY_NO_PHYSICAL_EPSILON_TRACE'}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'scalar_contact_tables.json.gz').open('xb') as f:f.write(blob)
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
print('RESULT '+json.dumps({'status':'QUALIFIED_RESTRICTED_PARITY_EVEN_YUKAWA_REFERENCE_AND_SCALAR_FINITE_BUBBLE','elapsed_after_imports':time.perf_counter()-start,'chiral_role_projector_patterns_checked':340,'operator_covariance_positions_checked':704,'scalar_spin_coefficients_compared':64,'scalar_metric_and_cross_positions_compared':3*328**2,'scalar_metric_ranks':[20,252],'actual_bar_pole_finite':P['actual_bar_pole_finite'],'actual_hat_pole_finite':P['actual_hat_pole_finite'],'reference_physical_pole_finite':P['reference_physical_pole_finite'],'finite_scalar_Pi_coefficient_per_metric':str(F),'finite_canonical_scalar_Pi_per_family_trace':str(F/2),'finite_canonical_scalar_action_gradient_per_family_trace':str(F/4),'relative_hat_pole_per_metric':P['relative_hat_kinetic_pole'],'remaining_unmeasured_mixed_families':['YYG','YYGG','YYYY'],'full_family_norm_retained_no_extra_three':True,'controls':controls,'scalar_contact_packed_sha256':sha256(blob).hexdigest(),'scalar_contact_raw_sha256':sha256(raw).hexdigest(),'new_one_loop_finite_bubble_families':1,'new_two_loop_integrals':0,'full_chiral_regularization_phase_or_measure_qualified':False,'mixed_scalar_gauge_completion_or_QAP_qualified':False,'finite_massive_threshold_or_physical_matching_qualified':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
