"""SRG1 parameter-plus-stationarity operators and independent closed response."""
from data import *
started=begin();guard('replay');mp.mp.dps=90
fc=packed(CAL/'canonical_so10_finite_counterterm_insertion/replay_v3_tables.json.gz')
fr=read(CAL/'canonical_so10_finite_counterterm_insertion/replay_v3_result.json')
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/replay_v3_tables.json.gz')
hr=read(CAL/'canonical_so10_heavy_tadpole_bridge/replay_v3_result.json')
sq=packed(CAL/'canonical_so10_scalar_quadratic_pullback/replay_tables.json.gz')
ut=read(CAL/'canonical_so10_uv_radial_tadpoles/primary_result.json')
M=dec(ht['raw_Hessian']);db=s.Matrix([20,25,0])
T={p:s.Matrix([red(s.sympify(z,locals={'w':w})/4) for z in ut[key]]) for p,key in zip(POWERS,['scalar_exact_reduced_w','mixed_fractional_exact','vector_fractional_exact'])}
# Solve by linear-system elimination, rather than use the native inverse.
d={p:tidy(s.Matrix(M).inv(method='GE')*T[p]) for p in POWERS}
vstat={p:tidy((db if p==2 else s.zeros(3,1))-d[p]) for p in POWERS}
out=[];minus=s.zeros(3,1);rm=dec(ht['Rminus2']);mixed=0;count=0
for ib,(b,ds) in enumerate(zip(fc['blocks'],ht['radial_blocks'])):
    m=b['multiplicity'];D=list(map(dec,ds['D']));Pg=dec(b['gauge']);jets=[];beta=weights(b['label']);count+=m*m
    for k,p in enumerate(POWERS):
        param=dec(sq['blocks']['Hpar'][ib]).subs(xi,1) if p==2 else dec(b['P'][k])
        Q=tidy(param+sum((vstat[p][j]*D[j] for j in range(3)),s.zeros(m)))
        zero(Pg*Q*Pg);mixed+=len(tidy(Q*Pg).todok());jets.append(Q)
    out.append({'block':ib,'stationary_pole_jets':list(map(enc,jets))})
    for a in range(3):
        for r,G in enumerate(b['gold_mass_projectors']):
            minus[a]=red(minus[a]+3*beta[a]*s.trace(dec(G)*dec(b['P'][0]))/s.Rational(fc['vector_mass_eigenvalues'][r]))
assert any(z!=0 for z in minus)
zero(minus-rm*d[0])
# Independent bisection for the exact Higgs-root branch used in the pole map.
point=read(CAL/'canonical_so10_positive_higgs/POINT.json')['determinant_polynomial']
A=mp.mpf(point['A']);B=mp.mpf(point['B0'])+mp.mpf(point['B1'])*mp.sqrt(15);C=mp.mpf(point['C0'])+mp.mpf(point['C1'])*mp.sqrt(15)
lo,hi=mp.mpf('.00530'),mp.mpf('.00531')
for _ in range(400):
    mid=(lo+hi)/2
    if A*mid*mid+B*mid+C>0:hi=mid
    else:lo=mid
root=(lo+hi)/2
R0=mp.matrix(hr['R0']);Rm=numeric(rm,root);dn={p:numeric(d[p],root) for p in POWERS};W={}
for p in ALLPOWERS:
    corr=mp.zeros(3,1)
    if p in POWERS:corr+=R0*dn[p]
    if p+2 in POWERS:corr+=Rm*dn[p+2]
    ans=2*(mp.matrix(fr['coefficients'][str(p)]['pole'])-corr)
    if p==-2:assert max(abs(z) for z in ans)<mp.mpf('1e-35');ans=mp.zeros(3,1) # EXACT identity above, not a small-value cutoff
    W[str(p)]=list(map(fmt,ans))
save('replay',{'method':'parameter_plus_stationary_motion_and_closed_pole_response','stationary_operators':out,
    'tadpole_CT':{str(p):list(map(str,T[p])) for p in POWERS},'stationary_VEV_pole':{str(p):list(map(str,vstat[p])) for p in POWERS},
    'W_coefficients':W,'matrix_slots':count,'goldstone_compression_positions':count*3,'mixed_orbit_column_nonzero':mixed,
    'inverse_g2_cancellation_proved_exactly':True,'finite_slope_read':False,'numerical_C1_calculated':False,
    'new_parameter_beta_obtained_from_finite_slope':False},started)
