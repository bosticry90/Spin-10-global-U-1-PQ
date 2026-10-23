"""FAN1 polarized Gram, independent charge transport and direct heavy EOM."""
from data import *
started=begin();guard('replay');mp.mp.dps=90
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/replay_v3_tables.json.gz')
hr=read(CAL/'canonical_so10_heavy_tadpole_bridge/replay_v3_result.json')
M=dec(ht['raw_Hessian']);metric=dec(ht['raw_metric'])
phy=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_replay.json')
O=dec(phy['vacuum']['orbit']);parts=[O[:54,:],O[54:306,:],O[326:328,:]];theta=[tidy(A.T*A) for A in parts]
wh=packed(CAL/'canonical_so10_width_hard_projection/replay_tables.json.gz');Pr=list(map(dec,wh['projectors'][1:]));lams=list(map(s.Rational,wh['eigenvalues'][1:]))
for T in theta:zero(T*dec(wh['projectors'][0]))
old=dec(phy['C3_plane_to_parent'])[:,:12];V=dec(packed(CAL/'canonical_so10_vector_quartic_ir_matching/replay_tables.json.gz')['light_embedding'])
Z=tidy((old.T*old).inv()*old.T*V);zero(old*Z-V);zero(V.T*V-s.eye(12))
charges=[tidy(Z.T*dec(B)*Z) for B in wh['H_charge_pairings'][1:]]
alph=[[clean(s.trace(P*T)/s.trace(P)) for T in theta] for P in Pr]
for P,ar in zip(Pr,alph):
    for T,a in zip(theta,ar):zero(T*P-a*P)
cp=s.Matrix([clean(sum(a[j]*s.trace(P) for a,P in zip(alph,Pr))/(2*metric[j,j])) for j in range(3)])
ct=s.Matrix([clean(sum(ar[j]*s.trace(P)*(L-U-s.log(lam/60)) for ar,P,lam in zip(alph,Pr,lams))/(2*metric[j,j])) for j in range(3)])
NF=[]
for j in range(3):
    # Independent scalar resolvent: -mass derivative of the coincident K^-1.
    e,x=s.symbols('eps x',positive=True)
    coef=-s.diff(s.gamma(1+e)*x**(-1-e)/12,x)
    assert s.simplify(coef-s.gamma(2+e)*x**(-2-e)/12)==0
    NF.append(tidy(sum((-ar[j]*B/(24*metric[j,j]*lam**2) for ar,B,lam in zip(alph,charges,lams)),s.zeros(12))))
gp=packed(CAL/'canonical_so10_nine_family_uv_assembly/replay_tables.json.gz');finite={}
assert all(s.sympify(z)==0 for z in gp['pole_assembly']['finite_L_squared_coefficient_inside_g2'])
mn=nm(M);R0=mp.matrix(hr['R0']);Rm=nm(dec(ht['Rminus2']))
for key,gg in [('1/2',mp.mpf('.5')),('1',mp.mpf(1))]:
    R=R0+Rm/gg;T=mp.zeros(3,1);TL=mp.zeros(3,1)
    for p in [0,2,4]:
        row=hr['tadpole_coefficients'][str(p)]
        T+=gg**(p//2)*(mp.matrix(row['constant'])+mp.log(gg)*mp.matrix(row['coupling_log']))
        TL+=gg**(p//2)*mp.matrix(row['scale_log'])
    h=mp.lu_solve(mn,-T);hl=mp.lu_solve(mn,-TL);B=R*h;BL=R*hl
    gcase=gp['finite_cases'][key]
    finite[key]=[[fmt(mp.mpf(gcase['known_graph_local_finite_L0'][i])+B[i]),fmt(mp.mpf(gcase['known_graph_local_scale_linear'][i])+BL[i]),'0'] for i in range(3)]
save('replay',{'method':'polarized_orbit_Gram_transported_charge_pairs_direct_EOM','theta':list(map(enc,theta)),
    'charges':list(map(enc,charges)),'sector_alpha':[[str(z) for z in row] for row in alph],
    'C_t_pole_over_g2':list(map(str,cp)),'C_t_finite_over_g2':list(map(str,ct)),'C_F2':list(map(enc,NF)),
    'first_width_radial_source_zero_positions':432,'second_width_curvature_positions':432,
    'source_left_derivative_coefficient':'1/2','finite_lambda2_fixed_xi':finite,'finite_C1_calculated':False,
    'full_two_loop_width_identity_qualified':False,'physical_target_read':False},started)
