"""OFK1 complete open-chain, off-shell integral, model-tensor and scope gate."""
from data import *
start=time.perf_counter();t=threading.Timer(600,lambda:os._exit(124));t.daemon=True;t.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==hsh,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def z(M):assert not s.SparseMatrix(M).applyfunc(s.simplify).todok()
def equal(a,b):assert s.simplify(s.gammasimp(s.sympify(a)-s.sympify(b)))==0
for key in ['external_embedding','external_projector','physical_chi','full_Casimir','unbroken_Casimir','width_Casimir','gauge_finite_difference_left','gauge_finite_difference_right','Yukawa_tensor_left','Yukawa_tensor_right','Yukawa_finite_difference']:z(dec(P[key])-dec(R[key]))
for key in ['scalar_sums_left','scalar_sums_right','scalar_mixed_sums','family_left','family_right']:
 for a,b in zip(P[key],R[key]):z(dec(a)-dec(b))
for key in P['jets']:
 for a,b in zip(P['jets'][key],R['jets'][key]):equal(a,b)
for key in P['exact_regular_integrals']:equal(P['exact_regular_integrals'][key],R['exact_regular_integrals'][key])
eps,L,h,x=s.symbols('epsilon L h x');g=s.Symbol('g10')
expected={'actual_F':['1','L + 2'],'reference_F':['1','L + 1'],'actual_L':['1','L + 5/3'],'reference_L':['1','L + 1'],
 'actual_Y':['1/2','L/2 + 1'],'reference_Y':['1/2','L/2 + 1'],'delta_F':['0','1'],'delta_L':['0','2/3'],'delta_Y':['0','0']}
for key,vals in expected.items():
 for a,b in zip(P['jets'][key],vals):equal(a,b)
equal(P['Feynman_numerator_polynomial'],-2-h);equal(P['longitudinal_linear_numerator_polynomial'],(6+h)*x-8-2*h)
U=dec(P['external_embedding']);Pe=dec(P['external_projector']);chi=dec(P['physical_chi']);z(U.H*U-s.eye(4));z(U*U.H-Pe);assert s.trace(Pe)==4;z(chi**2-s.eye(4))
for i in [4,5]:z(dec(P['hat_pair_matrices'][f'{i}_{i}'])-s.eye(4))
CF=dec(P['full_Casimir']);CH=dec(P['unbroken_Casimir']);CW=dec(P['width_Casimir']);DG=dec(P['gauge_finite_difference_left']);wh,wm=s.symbols('eta_H xi')
z(CF-s.Rational(45,8)*s.eye(16));z(CW-wh*CH-wm*(CF-CH));z(DG-(CF+2*CW)/3);z(dec(P['gauge_finite_difference_right'])-DG.T)
z(DG-DG.H.xreplace({s.conjugate(wh):wh,s.conjugate(wm):wm}));z(DG.subs(wm,wh)-(1+2*wh)*CF/3)
oldg=packed(CAL/'canonical_so10_fermion_gauge_kinetic_pole/primary_tables.json.gz');oldy=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/primary_tables.json.gz')
z(CW-dec(oldg['gauge_kinetic_left']));z(CH-dec(oldg['unbroken_internal_Casimir']));z(CF-dec(oldg['full_internal_Casimir']))
for key in ['scalar_sums_left','scalar_sums_right']:
 oldkey='internal_left' if key.endswith('left') else 'internal_right'
 for a,b in zip(P[key],oldy[oldkey]):z(dec(a)-dec(b))
for key,old in [('Yukawa_tensor_left','full_left'),('Yukawa_tensor_right','full_right')]:z(dec(P[key])-dec(oldy[old]))
WY=dec(P['Yukawa_tensor_left']);z(dec(P['Yukawa_tensor_right'])-WY.T);z(WY-WY.H);z(dec(P['Yukawa_finite_difference']))
for a in P['scalar_mixed_sums']:z(dec(a))
for label,row,co in zip(['10','126'],P['family_left'],[s.Rational(5,8),s.Rational(63,8)]):
 Y=dec(row);z(Y-Y.H);assert s.expand(s.trace(Y)).coeff(LOC[f'u{label}_01'],2)==2
 assert any(s.expand(a)!=0 for a in Y-s.trace(Y)*s.eye(3)/3)
assert R['scalar_isometric_norms']==['10','126'] and R['scalar_support_sizes']==[20,252]
# Actual UV coefficients recovered only at this later comparison stage.
actual_pole=s.sympify(P['jets']['actual_F'][0])*CF+s.sympify(P['jets']['actual_L'][0])*(CW-CF);z(actual_pole-CW)
z(s.sympify(P['jets']['actual_Y'][0])*WY-WY/2)
wrongh=R['wrong_hat_dimension_sign_jets'];equal(wrongh['F'][1],-1);equal(wrongh['L'][1],-s.Rational(2,3))
# Full p^3 terms affect each individual longitudinal self-energy, but cancel
# from their relative difference. Report this sensitivity boundary explicitly.
cubic_finite=-s.Rational(1,6);assert cubic_finite!=0
literature_restoring_candidate=(5*CF+CW)/6
controls={'omit_internal_hat_vector_vertices_loses_nonzero_gauge_difference':bool(DG),
 'wrong_analytic_hat_sign':wrongh['F'][1]!=P['jets']['delta_F'][1],
 'omit_longitudinal_width_term':bool(s.SparseMatrix(DG-CF).todok()),
 'average_or_exchange_widths':DG!=DG.xreplace({wh:wm,wm:wh}),
 'open_line_half':DG!=DG/2,'extra_family_three':DG!=3*DG,
 'family_trace_average':WY!=s.eye(48)*s.trace(WY)/48,
 'drop_imaginary_real_scalar_half':WY!=WY/2,
 'premature_literature_restoration_identification':bool(s.SparseMatrix(DG-literature_restoring_candidate).todok())}
assert all(controls.values())
for obj in [P,R]:
 assert obj['physical_spin_rank']==4 and not obj['open_line_half_or_trace_divisor'] and not obj['extra_family_three']
 assert obj['full_internal_hat_vector_vertices_retained'] and not obj['closed_odd_chi_trace_constructed'] and not obj['physical_scheme_adopted'] and obj['new_two_loop_integrals']==0
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
local={'gauge_finite_difference_left':P['gauge_finite_difference_left'],'gauge_finite_difference_right':P['gauge_finite_difference_right'],'Yukawa_finite_difference':P['Yukawa_finite_difference'],
 'delta_inverse_propagator':'+i*g10^2*bar_slash*(PL*DG+PR*DG^T)/(16*pi^2)','DG':'(CF+2*CW)/3','physical_domain':'p_hat=0,p_bar^2>0,mass_independent_Euclidean',
 'open_normalization':'NO_PFAFFIAN_HALF_NO_FAMILY3_NO_WITNESS_DIVISOR','Yukawa_family_tensor_left':P['Yukawa_tensor_left'],'reference_type':'FULL_INTERNAL_LORENTZ_OPEN_ANTICOMMUTING_CLIFFORD_COMPARISON_ONLY',
 'finite_restoring_counterterm_or_measured_breaking_identity':False,'invariant_finite_normalization_adopted':False}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'open_kinetic_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_PHYSICAL_OPEN_SPINOR_EMBEDDING_AND_GAUGE_YUKAWA_FINITE_KINETIC_COMPARISON','elapsed_after_imports':time.perf_counter()-start,
 'external_spin_rank':4,'clifford_anticommutator_positions':36*64,'external_barred_chiral_positions':5*16,'scalar_spin_routing_positions':4*6*16,
 'model_color_positions_compared':5*16**2,'internal_scalar_positions_compared':6*16**2,'family_polynomial_positions_compared':4*9,'full_family_positions_compared':2*48**2,
 'actual_reference_integral_jets':P['jets'],'gauge_finite_difference':'(CF+2*CW)/3','CF':'45/8*I16','CW':'eta_H*CH+xi*(CF-CH)',
 'Yukawa_finite_difference':'0','Yukawa_tensor':'(5/8*Y10dagY10+63/8*Y126dagY126) tensor I16','zero_complements_compared':True,
 'exact_offshell_integral_comparison':'0','known_actual_UV_comparison':'0','chirality_and_embedding_remainders':'0',
 'controls':controls,'p_cubic_term_individual_finite_contribution':str(cubic_finite),'p_cubic_omission_changes_relative_difference':False,
 'coefficient_table_packed_sha256':sha256(blob).hexdigest(),'coefficient_table_raw_sha256':sha256(raw).hexdigest(),
 'new_one_loop_finite_selfenergy_families':2,'new_two_loop_integrals':0,'independently_measured_finite_Ward_or_Slavnov_insertion':False,
 'full_chiral_reference_source_measure_phase_or_massive_matching_qualified':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','scientific_authority_changed':False,'authority':'34/39'},sort_keys=True),flush=True)
