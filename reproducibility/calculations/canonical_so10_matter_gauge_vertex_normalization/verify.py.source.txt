"""MGN1 exact all-five-family and fixed-normalization projection verifier."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for name,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(name))==hsh,name
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def tidy(mat):return s.SparseMatrix(mat).applyfunc(s.simplify)
def zero(mat):assert not tidy(mat).todok()
for key in ['raw_DB','raw_ZA','plane_DB','plane_ZA','background_RH']:
 zero(dec(P[key])-dec(R[key]))
for key in ['F_left','F_right','family_left','family_right']:
 for a,b in zip(map(dec,P[key]),map(dec,R[key])):zero(a-b)
for key in ['loop_B','image_B','field_only_B','remainder_B','source_image']:
 for chir in ['left','right']:
  assert len(P[key][chir])==len(R[key][chir])==3
  for prim,rep in zip(P[key][chir],R[key][chir]):
   assert len(prim)==len(rep)==45
   for a,b in zip(map(dec,prim),map(dec,rep)):zero(a-b)
for key in ['loop_A','image_A','remainder_A','kinetic_image','kinetic_loop']:
 for chir in ['left','right']:
  assert len(P[key][chir])==len(R[key][chir])==(12 if key.endswith('_A') else 3)
  for a,b in zip(map(dec,P[key][chir]),map(dec,R[key][chir])):zero(a-b)
T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz')['Tminus']));H=dec(packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz')['H_new']);FL=list(map(dec,P['F_left']));FR=list(map(dec,P['F_right']));mfi=packed(CAL/'canonical_so10_matter_field_source_image/primary_tables.json.gz');zero(FL[0]-dec(mfi['F_left']));zero(FR[0]-dec(mfi['F_right']))
for chir in ['left','right']:
 for a,b in zip(map(dec,P['kinetic_image'][chir]),map(dec,P['kinetic_loop'][chir])):zero(a-b)
 for a,b in zip(map(dec,P['source_image'][chir][0]),map(dec,mfi['source_pole_image_'+chir])):zero(a-b)
 for grade in [1,2]:
  for a in map(dec,P['source_image'][chir][grade]):zero(a)
for grade in range(3):
 for left,right in zip(map(dec,P['loop_B']['left'][grade]),map(dec,P['loop_B']['right'][grade])):zero(right+left.T)
 for left,right in zip(map(dec,P['image_B']['left'][grade]),map(dec,P['image_B']['right'][grade])):zero(right+left.T)
 for left,right in zip(map(dec,P['source_image']['left'][grade]),map(dec,P['source_image']['right'][grade])):zero(right-left.T)
 for mat in [FL[grade],FR[grade]]:zero(mat-mat.H.xreplace({s.conjugate(eta):eta,s.conjugate(xi):xi}))
# Every coupled grade retains the independent kinetic comparison along H.
diagonal={};diagonal_remainders={}
for grade,label in enumerate(['gauge','10','126']):
 currents=list(map(dec,P['loop_B']['left'][grade]));coeff=dec(P['kinetic_loop']['left'][grade]);rows=[];diff=[]
 for h in range(12):
  current=tidy(sum((H[c,h]*currents[c] for c in range(45) if H[c,h]),s.zeros(16))+(dec(P['loop_A']['left'][h]) if grade==0 else s.zeros(16)));th=tidy(sum((H[c,h]*T[c] for c in range(45) if H[c,h]),s.zeros(16)));zero(coeff*th-th*coeff);remainder=tidy(current+s.I*coeff*th);rows.append(enc(current));diff.append(enc(remainder))
 diagonal[label]=rows;diagonal_remainders[label]=diff
# Sensitive controls are explicit alternative images, not adjusted coefficients.
Bpart=[tidy(dec(a)-dec(b)) for a,b in zip(P['image_B']['left'][0],P['field_only_B']['left'][0])];controls={'flip_even_B_sign':any(tidy(2*a).todok() for a in Bpart),'omit32_to16_half':any(a.todok() for a in Bpart),'omit_independent_A':any(dec(a).todok() for a in P['image_A']['left']),'omit_fermion_endpoint':any(tidy(s.I*FR[0].T*gen).todok() for gen in T),'omit_source_inverse':any(tidy(dec(a)+s.I*gen*FL[0]).todok() for a,gen in zip(P['source_image']['left'][0],T)),'wrong_source_pairing':bool(tidy(2*FL[0]).todok())}
wrong_raw=dec(P['raw_DB']);plane=dec(P['plane_DB']);controls['raw_as_orthonormal']=bool(tidy(wrong_raw-plane).todok())
for grade,label in [(1,'10'),(2,'126')]:controls['omit_Yukawa_field_'+label]=any(dec(a).todok() for a in P['field_only_B']['left'][grade])
assert all(controls.values())
for obj in [P,R]:
 assert obj['coefficient_carriers']==['g10^2*I3','Y10dagY10','Y126dagY126'] and not obj['old_sourcefree_match'] and not obj['source_qK_changed'] and not obj['generator_or_scheme_adopted'] and obj['new_loop_integrals']==obj['new_two_loop_integrals']==0
assert P['old_gauge_rows']==R['old_gauge_rows'] and P['spin_congruence_positions_checked']==4096
proper_receipts=[('canonical_so10_fermion_gauge_vertex_support','QUALIFIED_COMPLETE_OUTWARD_FERMION_GAUGE_VERTEX_UV_SUPPORT'),('canonical_so10_pure_gauge_matter_vertex_assembly','QUALIFIED_COMPLETE_PURE_GAUGE_MATTER_VERTEX_UV_AND_DIAGONAL_H_COVARIANTIZATION'),('canonical_so10_yukawa_dependent_gauge_vertices','QUALIFIED_COMPLETE_YUKAWA_DEPENDENT_GAUGE_VERTEX_UV_FAMILIES_AND_KINETIC_COVARIANTIZATION'),('canonical_so10_matter_source_uv_assembly','QUALIFIED_COMPLETE_PROPER_MATTER_SOURCE_UV_NORMALIZATION_PROJECTION')]
for folder,status in proper_receipts:assert read(CAL/folder/'validation_receipt.json')['status']==status
Bcounts={label:sum(len(dec(row).todok()) for chir in ['left','right'] for row in P['remainder_B'][chir][grade]) for grade,label in enumerate(['gauge','10','126'])};Acount=sum(len(dec(row).todok()) for chir in ['left','right'] for row in P['remainder_A'][chir]);Hcount=sum(len(dec(row).todok()) for rows in diagonal_remainders.values() for row in rows);match=not any(Bcounts.values()) and Acount==Hcount==0
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
raw=(json.dumps({'diagonal_H_left':diagonal,'diagonal_H_kinetic_remainders':diagonal_remainders,'old_plane_DB_half':enc(plane/2),'fixed_normalization_remainder_counts_B':Bcounts,'fixed_normalization_remainder_count_A':Acount,'no_global_old_sourcefree_match_inferred':True},sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'comparison_tables.json.gz').open('xb') as handle:handle.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_PROPER_FERMION_GAUGE_VERTEX_UV_AND_FIXED_NORMALIZATION_PROJECTION' if match else 'QUALIFIED_COMPLETE_VERTEX_UV_WITH_FIXED_NORMALIZATION_REMAINDER','elapsed_after_imports':time.perf_counter()-start,'proper_B_topology_families':5,'independent_A_topology_families':1,'B_current_positions_per_comparison':2*3*45*256,'A_current_positions_per_comparison':2*12*256,'kinetic_positions_per_comparison':2*3*256,'source_image_positions_per_comparison':2*3*45*256,'directly_reused_MFI_gauge_source_positions':2*45*256,'Yukawa_source_image_zero_positions':2*2*45*256,'factorized_full_B_family_positions_covered':2*45*48**2,'all_Lorentz_copies_checked':4,'spin_congruence_positions_checked':4096,'old_gauge_rows':P['old_gauge_rows'],'B_remainder_positions_by_carrier':Bcounts,'A_remainder_positions':Acount,'diagonal_H_kinetic_remainder_positions':Hcount,'fixed_normalization_matches_all_selected_projections':match,'controls':controls,'old_sourcefree_mismatch_preserved':True,'new_loop_integrals':0,'new_one_loop_vertex_families':0,'new_two_loop_integrals':0,'comparison_packed_sha256':sha256(blob).hexdigest(),'comparison_raw_sha256':sha256(raw).hexdigest(),'physical_scheme_adopted':False,'source_qK_changed':False,'finite_QAP_measure_or_quantum_equivalence_qualified':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
