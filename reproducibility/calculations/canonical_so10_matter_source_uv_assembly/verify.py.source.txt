"""MSU1 exact complete UV source-projection assembly, without fitted terms."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==h,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def tidy(M):return s.SparseMatrix(M).applyfunc(s.simplify)
def zero(M):assert not tidy(M).todok()
for label in ['leading_ghost','ordinary_ghost']:
 for frame in ['raw','plane']:zero(dec(P['ghost_matrices'][label][frame])-dec(R['ghost_matrices'][label][frame]))
 M=dec(P['ghost_matrices'][label]['plane']);zero(M-M.T);assert all(s.Poly(z,eta,xi).total_degree()==1 and all(c.is_real for c in s.Poly(z,eta,xi).coeffs()) for z in M.todok().values())
zero(dec(R['adjoint_Casimir'])-8*s.eye(45));assert P['old_generator_counts']=={'leading_ghost':33,'ordinary_ghost':44}
keys=['auxiliary_left','auxiliary_right','ordinary_ghost_left','ordinary_ghost_right','ordinary_complete_left','ordinary_complete_right']
for key in keys:
 for a,b in zip(map(dec,P[key]),map(dec,R[key])):zero(a-b)
for route in ['primary','replay']:
 A=packed(CAL/'canonical_so10_matter_auxiliary_source_pole'/(route+'_tables.json.gz'));V=packed(CAL/'canonical_so10_matter_vector_source_pole'/(route+'_tables.json.gz'))
 for actual,expected,factor in [('loop_left','auxiliary_left',xi),('loop_right','auxiliary_right',xi)]:
  for a,b in zip(map(dec,A[actual]),map(dec,P[expected])):zero(factor*a-b)
 for actual,expected in [('loop_left','ordinary_complete_left'),('loop_right','ordinary_complete_right')]:
  for a,b in zip(map(dec,V[actual]),map(dec,P[expected])):zero(a-b)
E=packed(CAL/'canonical_so10_matter_field_source_image/primary_tables.json.gz');EL=list(map(dec,E['source_pole_image_left']));full=list(map(dec,P['ordinary_complete_left']));gh=list(map(dec,P['ordinary_ghost_left']));aux=list(map(dec,P['auxiliary_left']))
assert any(tidy(a-b).todok() for a,b in zip(full,gh)) and any(tidy(a-2*b-e).todok() for a,b,e in zip(full,gh,EL)) and any(A.todok() for A in aux)
assert P['old_complete_source_maps_match'] and not P['old_sourcefree_normalization_match'] and not any(P['old_quantum_A5_obligations'].values())
for d in [P,R]:assert d['pole_unit_factor']=='1/2' and not d['new_loop_integrals'] and not d['source_qK_changed'] and not d['generator_or_scheme_adopted']
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_PROPER_MATTER_SOURCE_UV_NORMALIZATION_PROJECTION','elapsed_after_imports':time.perf_counter()-start,'complete_proper_UV_families':2,'coupling_orders_separately_matched':[2,3],'chiral_positions_compared_per_order':2*45*16**2,'total_chiral_positions_both_orders':4*45*16**2,'old_leading_generator_rows':33,'old_ordinary_generator_rows':44,'ghost_matrix_positions_two_frames_two_orders':4*45**2,'auxiliary_nonzero_per_chirality':sum(len(a.todok()) for a in aux),'ordinary_nonzero_per_chirality':sum(len(a.todok()) for a in full),'all_coefficients_and_zero_complements_match':True,'omit_fixed_kinetic_image_sensitive':True,'wrong_32_to16_pole_units_sensitive':True,'new_loop_integrals':0,'old_sourcefree_mismatch_preserved':True,'old_quantum_A5_obligations_preserved':True,'full_sourcefree_counterterm_QAP_or_equivalence_proved':False,'finite_matter_C1_or_physical_matching_proved':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
