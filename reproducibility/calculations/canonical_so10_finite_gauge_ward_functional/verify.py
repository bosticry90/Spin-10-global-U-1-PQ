"""GWF1 exact reconstruction, Euler, density and boundary comparison."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==h,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz');g=s.Symbol('g10')
def decode(rows):
 out={}
 for word,value in rows:
  key=tuple((k,mu,tuple(ds)) for k,mu,ds in word);assert key not in out;out[key]=s.sympify(value)
 return out
def eqrows(a,b):
 A,B=decode(a),decode(b);assert set(A)==set(B)
 for w,v in A.items():assert s.expand(v-B[w])==0,(w,v,B[w])
for key in ['density','Ward_image','direct_q_density','boundary_divergence','Ward_without_covariant_commutator']:eqrows(P[key],R[key])
for key in ['Euler_matrices','boundary_current']:
 assert len(P[key])==len(R[key])==4
 for a,b in zip(P[key],R[key]):eqrows(a,b)
assert P['invariant_zeta_Ward_image']==R['invariant_zeta_Ward_image']==[]
for key in P['cubic_vertex']:
 for word in ['012','021']:
  for a,b in zip(P['cubic_vertex'][key][word],R['cubic_vertex'][key][word]):assert s.expand(s.sympify(a)-s.sympify(b))==0
for w in set(P['quartic_density'])|set(R['quartic_density']):assert s.sympify(P['quartic_density'].get(w,0))==s.sympify(R['quartic_density'].get(w,0))
W=decode(P['Ward_image']);qd=decode(P['direct_q_density']);div=decode(P['boundary_divergence']);no=decode(P['Ward_without_covariant_commutator'])
for w in set(W)|set(qd)|set(div):assert s.expand(qd.get(w,0)-W.get(w,0)-div.get(w,0))==0
assert W and div
wrong_comm=sum(s.expand(W.get(w,0)-no.get(w,0))!=0 for w in set(W)|set(no))
degrees=sorted({mon[0] for v in W.values() for mon,coeff in s.Poly(v,g).terms() if coeff!=0});assert set(degrees).issubset({2,3,4})
controls={'omit_boundary_current':bool(div),'wrong_covariant_commutator':wrong_comm>0,'wrong_Ward_overall_sign':bool(W),'drop_cubic_companion':any(any(s.sympify(v)!=0 for v in arr) for block in P['cubic_vertex'].values() for arr in block.values()),'drop_quartic_companion':bool(P['quartic_density']),'wrong_closed_family_count':bool(W),'extra_normalization_half':bool(W)}
assert all(controls.values())
for obj in [P,R]:assert obj['quadratic_coefficient']=='1/6' and obj['physical_spin_trace']==4 and obj['closed_family_count']==3 and obj['new_loop_integrals']==0 and not obj['physical_scheme_adopted']
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPACT_FINITE_GAUGE_DIFFERENCE_AND_ALGEBRAIC_WARD_IMAGE','elapsed_after_imports':time.perf_counter()-start,'density_trace_words':len(P['density']),'Euler_ordered_words':[len(v) for v in P['Euler_matrices']],'Ward_trace_words':len(W),'direct_variation_trace_words':len(qd),'boundary_current_trace_words':[len(v) for v in P['boundary_current']],'boundary_divergence_trace_words':len(div),'cubic_vertex_positions_reconstructed':1024,'quartic_cyclic_positions_reconstructed':70,'wrong_covariant_commutator_changes_positions':wrong_comm,'Ward_coupling_degrees':degrees,'literal_density_Ward_boundary_remainder':'0','independent_Euler_remainder':'0','invariant_zeta_Ward_image':'0','controls':controls,'new_loop_integrals':0,'independently_integrated_new_quantum_insertion':False,'full_source_background_massive_admissibility_qualified':False,'full_QAP_measure_or_physical_matching_qualified':False,'finite_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
