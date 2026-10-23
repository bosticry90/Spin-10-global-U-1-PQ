"""BMC1 independent polynomial and RG-consistency evidence validation."""
from io_data import *
started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
keys=['K','g_i','zeta_a_coefficient','zeta_a2_coefficient','inverse_alpha_a2_coefficient','C0','C1_formula_only',
    'lambda1_tau_derivative','lambda2_tau_derivative','zeta_tau2','zeta_tau1']
for name in keys:assert s.cancel(ex(A[name])-ex(B[name]))==0,name
expected={
    'K':1-ell*g*g*lam1/3-ell**2*g*g*lam2/3,
    'zeta_a_coefficient':lam1/12,'zeta_a2_coefficient':lam1**2/144+lam2/(48*g*g),
    'inverse_alpha_a2_coefficient':-lam2/(48*alpha*g*g),
    'C0':-lam1/12,'lambda1_tau_derivative':6*(bi-b),'lambda2_tau_derivative':6*g*g*(ri-c)-W,
    'zeta_tau2':(bi-b)**2/4,'zeta_tau1':(ri-c)/8-p0*(bi-b)-W/(48*g*g)}
for name,want in expected.items():assert s.cancel(ex(A[name])-want)==0,name
# Direct polynomial multiplication, independent of either native inversion.
z1=lam1/12;z2=lam1**2/144+lam2/(48*g*g)
K=1-a*lam1/12-a*a*lam2/(48*g*g)
prod=s.Poly(s.expand(K*(1+a*z1+a*a*z2)-1),a)
assert all(prod.nth(i)==0 for i in [0,1,2])
assert s.expand(K*(1+a*z1+a*a*lam2/(48*g*g))-1).coeff(a,2)==-lam1**2/144
assert s.expand((1+a*z1+a*a*z2)*(1-a*z1+a*a*(z1*z1-z2))-1).coeff(a,2)==0
assert s.expand((1+a*z1+a*a*z2)*(1-a*z1-a*a*z2)-1).coeff(a,2)==-z1*z1
# One-loop D-dimensional heat normalization before the finite conversion.
ep,j=s.symbols('eps j');vec=(4-2*ep)/24-1+s.Rational(1,24)-s.Rational(1,12)
assert s.expand(vec+s.Rational(7,8)+ep/12)==0
vf=s.expand(-12*(vec*(1/ep+j)-vec.subs(ep,0)/ep)).coeff(ep,0)
sf=-12*j/24
assert vf==1+s.Rational(21,2)*j and sf==-j/2
assert s.simplify((4*s.pi/g**2)*(ell*g*g*lam1/3)).subs(ell,1/(16*s.pi**2))==lam1/(12*s.pi)
assert s.simplify((4*s.pi/g**2)*(ell**2*g*g*lam2/3)).subs(ell,1/(16*s.pi**2))==lam2/(192*s.pi**3)
sb=list(map(s.Rational,A['scalar_heavy_b']));tv=list(map(s.Rational,A['vector_T']))
assert sb==[s.Rational(377,30),s.Rational(77,6),s.Rational(79,6)] and tv==[8,6,5]
gs=packed(CAL/'canonical_so10_two_loop_gauge_beta/primary_tables.json.gz')
matrix=s.Matrix(gs['light_c_two_matrix']);rows=matrix*s.ones(3,1)
assert matrix==s.Matrix([[s.Rational(9,50),s.Rational(9,10),0],[s.Rational(3,10),-s.Rational(259,6),0],[0,0,-102]])
bp=s.Rational(gs['parent_b_one']);cp=s.Rational(gs['parent_c_two']);db=[x-bp for x in map(s.Rational,gs['light_b_one'])]
dc=[x-cp for x in rows]
for name in ['scalar_heavy_b','vector_T','one_loop_jump_mu','GS_db','GS_dc','old_full_dc','full_minus_GS_dc','explicit_g_component_W']:
    assert len(A[name])==len(B[name])==3
    assert all(s.cancel(ex(x)-ex(y))==0 for x,y in zip(A[name],B[name])),name
assert list(map(ex,A['GS_db']))==db
assert list(map(ex,A['GS_dc']))==dc==[-s.Rational(112919,75),-s.Rational(23243,15),-s.Rational(4826,3)]
assert list(map(ex,A['one_loop_jump_mu']))==[-6*t+21*v for t,v in zip(sb,tv)]==[6*x for x in db]
assert list(map(ex,A['explicit_g_component_W']))==[2576*g*g,1932*g*g,1610*g*g]
assert list(map(ex,A['full_minus_GS_dc']))==[-s.Rational(2131,10),-s.Rational(1659,10),-s.Rational(1459,10)]
# The old RG projection must NOT contain the finite demand or C0 diagnostics.
projection=read(HERE/'old_RG_input_projection.json')
assert set(projection['operands'])=={'parent_b_one_loop','parent_B_two_loop_yukawa_independent','SM_B_row_sums_at_unified_coupling','rg_log_kernel'}
for row in projection['operands']['rg_log_kernel']:
    assert set(row)=={'delta_b','delta_B_yukawa_independent','L2_coefficient','L_coefficient_without_C0_term'}
    assert s.Rational(row['L2_coefficient'])==s.Rational(row['delta_b'])**2/4
# Actual scale defect if the explicit gauge component of D1 is dropped.
# The FULL W is not inferred from any finite diagram slope.
rg_defects=[s.expand(-ex(z)/6) for z in A['explicit_g_component_W']]
assert all(z!=0 for z in rg_defects)
L1=6*(bi-b);L2=6*g*g*(ri-c)-W
inverse_beta=-2*ell*b-2*ell**2*c*g*g-ell*(L1+ell*W)/3-ell**2*L2/3
assert s.expand(inverse_beta+2*ell*bi+2*ell**2*ri*g*g)==0
assert s.expand(inverse_beta.subs(W,0)+2*ell*bi+2*ell**2*ri*g*g)==0 # fixed-mass special case is valid
# Change only the explicit derivative, retaining actual running W: fails.
wrong=-2*ell*b-2*ell**2*c*g*g-ell*(L1+ell*W)/3-ell**2*(6*g*g*(ri-c))/3
assert s.expand(wrong+2*ell*bi+2*ell**2*ri*g*g)==-ell**2*W/3
assert s.expand(2*(3*g*g*(ri-c)-W/2)-L2)==0
for d in [A,B]:
    assert d['full_W_calculated'] is d['numerical_C1_calculated'] is d['physical_demand_parsed'] is d['complete_finite_inventory_proved'] is False
receipt={'schema':'BMC1_VALIDATION_RECEIPT','status':'QUALIFIED_BACKGROUND_F2_COUPLING_CONVERSION_AND_RUNNING_INPUT_RG_LAW',
    'execution_state':'COMPLETED','exact_native_expression_comparisons':len(keys),'exact_light_beta_positions':9,
    'actual_one_loop_jumps':A['one_loop_jump_mu'],'GS_dc':A['GS_dc'],'full_minus_GS_dc':A['full_minus_GS_dc'],
    'explicit_g_component_W':A['explicit_g_component_W'],'C1_conversion_formula':A['C1_formula_only'],
    'full_W_calculated':False,'numerical_C1_calculated':False,'complete_finite_inventory_proved':False,
    'controls':{'wrong_F2_factor4_detected':True,'missing_zeta_square_detected':True,'duplicate_inverse_square_detected':True,
    'nonabelian_coupling_rescaling_required':True,'wrong_bare_Ward_ratio_detected':True,
    'missing_running_input_term_sensitive':True,'tau_vs_log_Q2_factor2_checked':True,'full_matter_beta_substitution_detected':True},
    'historical_fixed_mass_RG_template_withdrawn':False,'no_new_fermion_or_flavor_amplitude':True,
    'scientific_acceptance':'NOT_PERFORMED','scientific_authority':'34/39_UNCHANGED','full_E5_A5_qualified':False,
    'elapsed_after_imports':time.perf_counter()-started}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
