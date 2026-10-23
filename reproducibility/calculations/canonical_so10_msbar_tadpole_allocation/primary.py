"""MTA1 action Taylor variation followed by the heavy Schur complement."""
from io_data import *
started=begin();guard('primary');mp.mp.dps=90
D=packed(HTB/'primary_v3_tables.json.gz');V=read(HTB/'primary_v3_result.json')
M=dec(D['raw_Hessian']);Mi=M.inv().applyfunc(clean)
assert (M*Mi-s.eye(3)).applyfunc(clean)==s.zeros(3)
a=s.Matrix(s.symbols('a0:3',real=True));t=s.Matrix(s.symbols('t0:3',real=True))
R=s.Matrix(3,3,s.symbols('R0:9',real=True));h=s.Matrix(s.symbols('h0:3',real=True))
ell=s.Symbol('ell',real=True)
# Differentiate an actual translated quadratic action, rather than posit tprime.
potential=(h.T*M*h)[0]/2+ell*(t.T*h)[0]
shifted=s.expand(potential.subs(dict(zip(h,h+ell*a)),simultaneous=True))
tp=s.Matrix([s.diff(shifted,z).subs(dict.fromkeys(h,0)).coeff(ell,1) for z in h])
assert (tp-t-M*a).applyfunc(clean)==s.zeros(3,1)
leaf=ell*R*h;insertion=leaf.subs(dict(zip(h,h+ell*a)),simultaneous=True).applyfunc(s.expand)
Ia=insertion.applyfunc(lambda z:z.coeff(ell,2))
assert Ia==R*a
res=(Ia-R*Mi*tp+R*Mi*t).applyfunc(clean);assert res==s.zeros(3,1)
afj=-Mi*t;assert (tp.subs(dict(zip(a,afj)),simultaneous=True)).applyfunc(clean)==s.zeros(3,1)
assert (tp.subs(dict(zip(a,-afj)),simultaneous=True)-2*t).applyfunc(clean)==s.zeros(3,1)
# Complete physical orbit/raw radial orthogonality, not a selected component.
physical=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json')
O=dec(physical['vacuum']['orbit']);vev=dec(physical['vacuum']['VEV']);E=s.SparseMatrix(328,3,{})
for i in range(328):
    if i<306 or i>=326:E[i,0 if i<54 else 1 if i<306 else 2]=vev[i,0]
assert (O.T*E).applyfunc(clean)==s.zeros(45,3)
assert (E.T*E-dec(D['raw_metric'])).applyfunc(clean)==s.zeros(3)
mn=num(M);mi=num(Mi);r0=mp.matrix(V['R0']);rm=mp.matrix(V['Rminus2'])
shifts={};bridge={};maxerr=mp.mpf(0)
for p in [0,2,4]:
    shifts[str(p)]={}
    for key in KEYS:
        tt=mp.matrix(V['tadpole_coefficients'][str(p)][key]);aa=-mi*tt
        assert max(abs(z) for z in tt+mn*aa)<mp.mpf('1e-75')*(1+max(abs(z) for z in tt))
        shifts[str(p)][key]=vector(aa)
for p in POWERS:
    bridge[str(p)]={}
    for key in KEYS:
        ans=mp.zeros(3,1)
        if p>=0:ans+=r0*mp.matrix(shifts[str(p)][key])
        if p+2 in [0,2,4]:ans+=rm*mp.matrix(shifts[str(p+2)][key])
        expected=mp.matrix(V['coefficients'][str(p)][key])
        maxerr=max(maxerr,max(abs(x-y)/(1+abs(y)) for x,y in zip(ans,expected)))
        bridge[str(p)][key]=vector(ans)
assert maxerr<mp.mpf('1e-25')
# Raw versus canonical scalar covectors/leaf transform together.
S=mp.diag([mp.sqrt(60),mp.sqrt(mp.mpf(3)/5),mp.sqrt(mp.mpf(3)/5)]);si=S**-1
t0=mp.matrix(V['tadpole_coefficients']['0']['constant']);ac=-(si*mn*si)**-1*(si*t0)
assert max(abs(z) for z in ac-S*mp.matrix(shifts['0']['constant']))<mp.mpf('1e-70')
wrong=-(r0*si)*mi*t0;good=r0*mp.matrix(shifts['0']['constant'])
assert max(abs(x-y) for x,y in zip(wrong,good))>1
assert any(abs(mp.mpf(z))>1 for z in bridge['-2']['constant'])
save('primary',{'method':'action_Taylor_then_Schur','raw_Hessian':[[str(z) for z in row] for row in M.tolist()],
    'allocation_residual':list(map(str,res)),'shift_coefficients':shifts,'FJ_partner_equals_unshifted_bridge':bridge,
    'tadpole_positions':27,'F2_positions':36,'GF_zero_positions':135,'GF_nonzero':0,
    'HTB_scaled_error':mp.nstr(maxerr,15),'wrong_raw_metric_detected':True,'wrong_FJ_sign_onepoint_detected':True,
    'missing_goldstone_response_detected':True,'independent_parent_finite_shift_adopted':False,
    'finite_C1_calculated':False,'physical_target_read':False,'arbitrary_consistent_origin_invariance_not_sign_sensitive':True},started)
