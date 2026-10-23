"""MTA1 parent potential differentiation and direct translated EOM solve."""
from io_data import *
started=begin();guard('replay');mp.mp.dps=90
D=packed(HTB/'replay_v3_tables.json.gz');V=read(HTB/'replay_v3_result.json')
# Reconstruct the parent neutral restriction from the actual frozen point.
base=read(CAL/'canonical_so10_scalar_benchmark/STAGE1_POINT.json')['free_coefficients']
base.update(read(CAL/'canonical_so10_positive_higgs/POINT.json')['changed_free_coefficients'])
c={k:s.Rational(v) for k,v in base.items() if ':' not in k}
x,y,z=s.symbols('x y z',real=True);w0=s.sqrt(60);sig=s.sqrt(s.Rational(3,5))
lp=c['lambdaPhi1']+s.Rational(7,60)*c['lambdaPhi2'];lm=c['lambdaPhiSigma1']-c['lambdaPhiSigma2']/4
potential=c['muPhi']*x**3+lp*x**4+lm*x*x*y*y+c['lambdaPhiS']*x*x*z*z/2+c['lambdaSigma1']*y**4+c['lambdaSigmaS']*y*y*z*z/2+c['lambdaS']*z**4/4
m0,m1,m2=s.symbols('m0:3');potential+=m0*x*x+m1*y*y+m2*z*z/2
at={x:w0,y:sig,z:sig};masses=s.solve([s.diff(potential,q).subs(at) for q in [x,y,z]],[m0,m1,m2])
potential=potential.subs(masses);r=s.Matrix(s.symbols('r0:3',real=True))
fractional=s.expand(potential.subs({x:w0*r[0],y:sig*r[1],z:sig*r[2]}))
M=s.hessian(fractional,r).subs(dict.fromkeys(r,1)).applyfunc(clean)
assert (M-dec(D['raw_Hessian'])).applyfunc(clean)==s.zeros(3)
a=s.Matrix(s.symbols('a0:3',real=True));tt=s.Matrix(s.symbols('t0:3',real=True));ell=s.Symbol('ell',real=True)
grad=s.Matrix([s.diff(fractional,q) for q in r]);translated=grad.subs(dict(zip(r,s.ones(3,1)+ell*a)),simultaneous=True)
onepoint=translated.applyfunc(lambda z:s.diff(z,ell).subs(ell,0))+tt
assert (onepoint-tt-M*a).applyfunc(clean)==s.zeros(3,1)
sol=s.solve(list(onepoint),list(a));afj=s.Matrix([sol[q] for q in a])
assert (M*afj+tt).applyfunc(clean)==s.zeros(3,1)
# Directly solve translated heavy stationarity, retaining arbitrary origin a.
b=s.Matrix(s.symbols('b0:3',real=True));bs=s.solve(list(M*(b+a)+tt),list(b))
absolute=s.Matrix([bs[q] for q in b])+a
R=s.Matrix(3,3,s.symbols('u0:9',real=True));absolute_leaf=(R*absolute).applyfunc(clean)
assert (absolute_leaf-R*afj).applyfunc(clean)==s.zeros(3,1)
# Independently normalized canonical-coordinate linear solve, no cached inverse.
S=mp.diag([mp.sqrt(60),mp.sqrt(mp.mpf(3)/5),mp.sqrt(mp.mpf(3)/5)]);Si=S**-1
mn=num(M);mc=Si*mn*Si;r0=mp.matrix(V['R0'])*Si;rm=mp.matrix(V['Rminus2'])*Si
shifts={};bridge={};err=mp.mpf(0)
for p in [0,2,4]:
    shifts[str(p)]={}
    for key in KEYS:
        tcan=Si*mp.matrix(V['tadpole_coefficients'][str(p)][key]);ac=mp.lu_solve(mc,-tcan)
        assert max(abs(z) for z in mc*ac+tcan)<mp.mpf('1e-75')*(1+max(abs(z) for z in tcan))
        shifts[str(p)][key]=vector(Si*ac)
for p in POWERS:
    bridge[str(p)]={}
    for key in KEYS:
        v=mp.zeros(3,1)
        if p>=0:v+=r0*S*mp.matrix(shifts[str(p)][key])
        if p+2 in [0,2,4]:v+=rm*S*mp.matrix(shifts[str(p+2)][key])
        e=mp.matrix(V['coefficients'][str(p)][key]);err=max(err,max(abs(x-y)/(1+abs(y)) for x,y in zip(v,e)))
        bridge[str(p)][key]=vector(v)
assert err<mp.mpf('1e-25')
# GF projection from direct sparse coefficient contractions using the replay.
physical=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_replay.json')
vev={i:s.sympify(z) for i,j,z in physical['vacuum']['VEV']['entries']};ort=s.zeros(45,3)
for i,j,z0 in physical['vacuum']['orbit']['entries']:
    if i in vev and (i<306 or i>=326):ort[j,0 if i<54 else 1 if i<306 else 2]+=s.sympify(z0)*vev[i]
assert ort.applyfunc(clean)==s.zeros(45,3)
save('replay',{'method':'parent_polynomial_gradient_and_direct_EOM_canonical_solve',
    'raw_Hessian':[[str(z) for z in row] for row in M.tolist()],
    'allocation_residual':['0']*3,'shift_coefficients':shifts,'FJ_partner_equals_unshifted_bridge':bridge,
    'tadpole_positions':27,'F2_positions':36,'GF_zero_positions':135,'GF_nonzero':0,
    'HTB_scaled_error':mp.nstr(err,15),'parent_neutral_potential_reconstructed':True,
    'independent_parent_finite_shift_adopted':False,'finite_C1_calculated':False,'physical_target_read':False,
    'arbitrary_consistent_origin_invariance_not_sign_sensitive':True},started)
