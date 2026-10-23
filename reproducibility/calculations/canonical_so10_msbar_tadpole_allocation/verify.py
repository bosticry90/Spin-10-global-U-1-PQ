"""MTA1 separate adjugate, action-source, allocation and mutation validation."""
from io_data import *
from itertools import permutations
started=begin('validation_preparation.json');mp.mp.dps=100
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
contract=read(ROOT/'tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.json')
assert contract['counterterm_contract_sha256']=='87cf0b4966451c62168552284cb1c709c5e3247d8e1b8241e34d4b78116c48f1'
assert contract['scheme']['subtraction']=='MSbar'
assert contract['scheme']['tadpole_VEV_prescription']==('FJ_like_explicit_tadpole_shift: parent parameters remain MSbar; '
    'v0=Z_background_scalar^(1/2)*(v+Delta_v); Delta_v and delta_t '
    'are fixed from the same renormalized one_point conditions and '
    'are used in scalar, Goldstone, ghost, and vector sectors')
assert len(contract['parent_operator_basis']['rows'])==29
assert contract['parent_operator_basis']['real_Hermitian_directions']==34
assert contract['all_slot_pole_residues_derived'] is False
assert read(ROOT/'tools/two_loop_qft_compiler_v1/layer5_counterterm_independent_replay.json')['qualification']==('structural bare-action expansion only; one-loop pole residues remain uncalculated')
M=s.Matrix(A['raw_Hessian']);assert (M-s.Matrix(B['raw_Hessian'])).applyfunc(clean)==s.zeros(3)
assert M==s.Matrix([[s.Rational(5033109,312500)-s.Rational(7043823,2500000)*s.sqrt(15),s.Rational(-112797,25000000),0],
    [s.Rational(-112797,25000000),s.Rational(280840437,156250000),0],[0,0,s.Rational(18,25)]])
# Explicit cofactors/adjugate; no native inverse, solve, or cached inverse used.
cof=s.Matrix(3,3,lambda i,j:(-1)**(i+j)*M.minor_submatrix(i,j).det())
det=sum(M[0,j]*cof[0,j] for j in range(3));adj=cof.T
assert (M*adj-det*s.eye(3)).applyfunc(clean)==s.zeros(3)
mi=num(adj.applyfunc(lambda z:clean(z/det)));mn=num(M)
e=s.Matrix(s.symbols('e0:3'));t=s.Matrix(s.symbols('v0:3'));r=s.Matrix(3,3,s.symbols('r0:9'))
inverse=adj/det
assert (r*e-r*inverse*(t+M*e)+r*inverse*t).applyfunc(clean)==s.zeros(3,1)
assert (r*e).applyfunc(clean)!=s.zeros(3,1)
assert (t+M*(inverse*t)-2*t).applyfunc(clean)==s.zeros(3,1)
# Pole/evanescent allocation must be combined before the finite extraction.
ep,pc,tf,rr0,rr1=s.symbols('eps pole tf R0 R1')
assert s.expand((pc/ep+tf-pc/ep)*(rr0+ep*rr1)).coeff(ep,0)==tf*rr0
assert s.expand((pc/ep+tf-2*pc/ep)*(rr0+ep*rr1)).coeff(ep,0)==tf*rr0-pc*rr1
maxerr=mp.mpf(0);shiftcount=0;fcount=0;zero_shift=0;zero_f2=0
actual=read(HTB/'primary_v3_result.json');D=packed(HTB/'primary_v3_tables.json.gz')
rm=num(dec(D['Rminus2']));r0=mp.matrix(actual['R0'])
assert max(abs(x-y) for x,y in zip(rm,mp.matrix(actual['Rminus2'])))<mp.mpf('1e-35')
shifts={}
def near(x,y):
    global maxerr
    z=abs(x-y)/(1+abs(y));maxerr=max(maxerr,z);assert z<mp.mpf('1e-25')
for p in [0,2,4]:
    shifts[p]={}
    for key in KEYS:
        tt=mp.matrix(actual['tadpole_coefficients'][str(p)][key]);v=-mi*tt;shifts[p][key]=v
        for j in range(3):
            for data in [A,B]:near(mp.mpf(data['shift_coefficients'][str(p)][key][j]),v[j])
            near((mn*v+tt)[j],0);zero_shift+=int(v[j]==0);shiftcount+=1
missing_partner=[];omitted_gold=[]
for p in POWERS:
    for key in KEYS:
        v=mp.zeros(3,1);gold=mp.zeros(3,1)
        if p in shifts:v+=r0*shifts[p][key]
        if p+2 in shifts:gold=rm*shifts[p+2][key];v+=gold
        for j in range(3):
            for data in [A,B]:near(mp.mpf(data['FJ_partner_equals_unshifted_bridge'][str(p)][key][j]),v[j])
            near(mp.mpf(actual['coefficients'][str(p)][key][j]),v[j]);zero_f2+=int(v[j]==0);fcount+=1
        missing_partner+=list(v);omitted_gold+=list(gold)
assert shiftcount==27 and fcount==36
assert max(abs(z) for z in missing_partner)>1 and max(abs(z) for z in omitted_gold)>1
# Exact nonzero map detects unpaired finite tadpoles and Goldstone omission.
goldmap=(-dec(D['Rminus2'])*inverse).applyfunc(clean)
assert any(z!=0 for z in goldmap)
assert goldmap==dec(D['Rminus2_tadpole_linear_map'])
# Independent raw/canonical comparison on every tadpole coefficient.
S=mp.diag([mp.sqrt(60),mp.sqrt(mp.mpf(3)/5),mp.sqrt(mp.mpf(3)/5)]);si=S**-1
for p in [0,2,4]:
    for key in KEYS:
        tt=mp.matrix(actual['tadpole_coefficients'][str(p)][key]);aa=mp.lu_solve(si*mn*si,-si*tt)
        for x,y in zip(si*aa,shifts[p][key]):near(x,y)
wrong=-r0*mi*si*mp.matrix(actual['tadpole_coefficients']['0']['constant'])
right=r0*shifts[0]['constant'];assert max(abs(x-y) for x,y in zip(wrong,right))>1
for data in [A,B]:
    assert data['allocation_residual']==['0']*3 and data['GF_zero_positions']==135 and data['GF_nonzero']==0
    assert data['finite_C1_calculated'] is False and data['independent_parent_finite_shift_adopted'] is False
    assert data['physical_target_read'] is False and data['arbitrary_consistent_origin_invariance_not_sign_sensitive']
assert B['parent_neutral_potential_reconstructed'] and A['wrong_FJ_sign_onepoint_detected']
# Recover orbit orthogonality from sparse row dot-products without native helpers.
phy=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json')
ev={i:s.sympify(z) for i,j,z in phy['vacuum']['VEV']['entries']};dots=[[0]*3 for _ in range(45)]
for i,j,z in phy['vacuum']['orbit']['entries']:
    if i in ev and (i<306 or i>=326):dots[j][0 if i<54 else 1 if i<306 else 2]+=s.sympify(z)*ev[i]
assert all(clean(z)==0 for row in dots for z in row)
controls={'omitted_partner_detected':True,'double_bridge_after_FJ_detected':True,
    'wrong_FJ_sign_by_onepoint_detected':True,'wrong_sign_not_detectable_from_paired_total_alone':True,
    'omitted_actual_Goldstone_inverse_g2_detected':True,'raw_canonical_covector_mix_detected':True,
    'double_pole_tadpole_CT_detected':True,'unpaired_finite_tadpole_changes_selected_answer':True}
out={'schema':'MTA1_VALIDATION_RECEIPT','status':'QUALIFIED_MSBAR_PARENT_CONSTRAINT_AND_CORRELATED_RADIAL_TADPOLE_ALLOCATION',
    'execution_state':'COMPLETED','finite_parent_scalar_input_changes_authorized':False,
    'parent_MSbar_directions':34,'original_compiler_roundtrip_structural_only':True,
    'tadpole_positions':shiftcount,'F2_positions':fcount,'zero_shift_positions':zero_shift,'zero_F2_positions':zero_f2,
    'GF_zero_positions':135,'numerical_scaled_error':mp.nstr(maxerr,15),'numerical_tolerance':'1e-25',
    'controls':controls,'HTB_bridge_retained_exactly_once':True,'FJ_shift_formal_not_controlled_vacuum':True,
    'partial_BFM_to_BFT_gauge_equivalence_proved':False,'full_finite_C1_calculated':False,
    'full_finite_input_framework_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority_changed':False,
    'elapsed_after_imports':time.perf_counter()-started}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
