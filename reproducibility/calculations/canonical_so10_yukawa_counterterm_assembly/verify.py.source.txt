"""YCA1 exact comparison, covariance and complete tensor-factor closure."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==h,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def tidy(M):return s.SparseMatrix(M).applyfunc(s.expand)
def zero(M):assert not tidy(M).todok()
def differs(M):assert tidy(M).todok()
zero(dec(P['W'])-dec(R['W']));zero(dec(P['Z_F_Y'])-dec(R['Z_F_Y']))
ys=[];poles=[];traces=[];units=[s.Rational(5,8),s.Rational(63,8)];rows=[]
for p,r in zip(P['models'],R['models']):
 for key in ['Y','fermion_field_image','scalar_field_image','Yukawa_pole','gauge_pole','full_pole']:zero(dec(p[key])-dec(r[key]))
 assert p['trace']==r['trace'] and p['scalar_metric_unit']==r['scalar_metric_unit']=='1/2'
 y=dec(p['Y']);d=dec(p['full_pole']);zero(y-y.T);zero(d-d.T)
 ys.append(y);poles.append(d);traces.append(s.sympify(p['trace'],locals=LOC))
 # Correct scalar family trace contains each independent off-diagonal twice.
 k=sum((1 if i==j else 2)*(LOC[f'u{p["R"]}_{i}{j}']**2+LOC[f'v{p["R"]}_{i}{j}']**2) for i in range(3) for j in range(i,3));assert s.expand(k-traces[-1])==0
 for z in d.todok().values():assert {sum(m) for m in s.Poly(z,*LOC.values()).monoms()}=={3}
 rows.append({'R':p['R'],'complex_positions':9,'nonzero_positions':len(d.todok()),'monomials_full_matrix':sum(len(s.Poly(z,*LOC.values()).terms()) for z in d.todok().values())})
W=dec(P['W']);expected=sum((u*y.H*y for u,y in zip(units,ys)),s.zeros(3));zero(W-expected);zero(W-W.H)
for y,k,d,p in zip(ys,traces,poles,P['models']):
 yp=(W.T*y+y*W+k*y)/4;zero(dec(p['Yukawa_pole'])-yp);zero(d-yp+s.Rational(135,8)*G**2*y)
 differs((W*y+y*W+k*y)/4-yp) # Wrong transpose on first fermion field.
 differs((W.H*y+y*W+k*y)/4-yp)
 differs((W.T*y+k*y)/4-yp);differs((y*W+k*y)/4-yp)
 differs((W.T*y+y*W)/4-yp);differs((3*W.T*y+3*y*W+3*k*y)/4-yp)
 diagonaltrace=sum(y[i,i]*s.conjugate(y[i,i]) for i in range(3));differs((diagonaltrace-k)*y/4)
 averaged=s.trace(W)*s.eye(3)/3;differs((averaged.T*y+y*averaged-W.T*y-y*W)/4)
 # The formula's conjugate density is transported by the conjugated maps.
 zero(d.conjugate()-((W.conjugate().T*y.conjugate()+y.conjugate()*W.conjugate()+k*y.conjugate())/4-s.Rational(135,8)*G**2*y.conjugate()))
# Constant-unitary general law is proved in DERIVATION, using U*U^T=I.
# Exact nonreal and three-family permutation diagnostics check implementation.
Us=[s.Matrix([[3,4*s.I,0],[4*s.I,3,0],[0,0,5]])/5,s.Matrix([[0,1,0],[0,0,1],[1,0,0]])]
covariance_positions=0
for U in Us:
 zero(U.H*U-s.eye(3));zero(U.conjugate()*U.T-s.eye(3));new=[tidy(U.T*y*U) for y in ys]
 subs={}
 for p,n in zip(P['models'],new):
  for i in range(3):
   for j in range(i,3):subs[LOC[f'u{p["R"]}_{i}{j}']]=s.expand(s.re(n[i,j]));subs[LOC[f'v{p["R"]}_{i}{j}']]=s.expand(s.im(n[i,j]))
 zero(W.xreplace(subs)-U.H*W*U)
 for d,k in zip(poles,traces):
  zero(d.xreplace(subs)-U.T*d*U);assert s.expand(k.xreplace(subs)-k)==0;covariance_positions+=9
yc=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');yr=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz')
hm=packed(CAL/'canonical_so10_fermion_kinetic_mass_poles/primary_tables.json.gz');hs=list(map(dec,hm['scalar_metrics']))
f=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/primary_tables.json.gz');fr=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/replay_tables.json.gz')
for item in [f,fr]:
 zero(dec(item['full_left'])-s.kronecker_product(W,s.eye(16)));zero(dec(item['full_right'])-s.kronecker_product(W.T,s.eye(16)))
permutation=s.SparseMatrix(256,256,{(16*i+j,16*j+i):1 for i in range(16) for j in range(16)})
for r,key in enumerate(['B10','B126']):
 b=dec(yc[key]);zero(b-dec(yr[key]));zero(permutation*b-b)
 for t,h in enumerate(hs):zero(b*h-(b/2 if r==t else s.zeros(256,328)))
zero(dec(hm['cross_scalar_metric']))
gg=packed(CAL/'canonical_so10_gauge_yukawa_vertex_poles/primary_tables.json.gz');ci=dec(gg['fermion_Casimir_I_H'][0]);zero(ci-s.Rational(45,8)*s.eye(16))
gr=read(CAL/'canonical_so10_gauge_yukawa_vertex_poles/validation_receipt_v2.json');assert gr['parameter_field_positions_checked']==167936
for p in gr['parameter_counterterms']:assert p['parameter_pole_coefficient']=='-135/8' and p['width_independent']
for D in [P,R]:assert D['new_loop_integrals']==0 and not D['finite_scheme_or_flavor_adopted'] and D['proper_Yukawa_vertex_UV_pole']=='0'
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
print('RESULT '+json.dumps({'status':'QUALIFIED_FULL_ONE_LOOP_YUKAWA_PARAMETER_POLE_ASSEMBLY','elapsed_after_imports':time.perf_counter()-start,'complex_matrix_positions_compared':18,'separated_matrix_polynomial_positions_compared':2*6*9,'family_real_coordinates':24,'models':rows,
 'counterterm_stripped':'(W^T*Y_R+Y_R*W+Tr(Y_R^dagger*Y_R)*Y_R)/4-(135/8)*g10^2*Y_R','W':'(5/8)*Y10^dagger*Y10+(63/8)*Y126^dagger*Y126','normalization':'1/(16*pi^2*epsilon)',
 'offdiagonal_trace_weight':2,'unitary_diagnostic_positions':covariance_positions,'general_unitary_covariance_basis':'ALGEBRAIC_UNITARY_CONGRUENCE_PROOF_AND_EXACT_DIAGNOSTICS','carrier_positions_checked':167936,'metric_carrier_products_checked':335872,'structural_family_internal_scalar_slots':1511424,'full_polynomial_array_expanded':False,
 'negative_controls':['first_leg_transpose','first_leg_conjugation','either_fermion_half_omission','scalar_half_omission','extra_family3','offdiagonal_trace_loss','family_matrix_replaced_by_average_trace'],
 'new_loop_integrals':0,'new_two_loop_integrals':0,'hat_scalar_pole_retained_separately':True,'beta_function_claimed':False,'mass_source_VEV_or_tadpole_counterterms_qualified':False,'finite_hatted_field_source_completion_qualified':False,'full_forest_QAP_or_physical_matching_qualified':False,'physical_flavor_or_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
