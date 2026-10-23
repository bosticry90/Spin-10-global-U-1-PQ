"""FAN1 ordered source vertices, actual adjoint charge images and family sum."""
from data import *
started=begin();guard('primary');mp.mp.dps=90
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_tables.json.gz')
hr=read(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_result.json')
M=dec(ht['raw_Hessian']);metric=dec(ht['raw_metric']);Mi=tidy(M.inv())
bf=packed(CAL/'canonical_so10_background_threshold_inputs/primary_tables.json.gz')
phy=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json')
v=dec(phy['vacuum']['VEV']);theta=[s.SparseMatrix(45,45,{}) for _ in range(3)]
for a,b,i,z in bf['T']:
    if v[i,0]!=0 and (i<306 or i>=326):theta[0 if i<54 else 1 if i<306 else 2][a,b]+=s.sympify(z)*v[i,0]
theta=list(map(tidy,theta));assert theta[2]==s.zeros(45)
for T in theta:zero(T-T.T)
wh=packed(CAL/'canonical_so10_width_hard_projection/primary_tables.json.gz');Pr=list(map(dec,wh['projectors'][1:]));lams=list(map(s.Rational,wh['eigenvalues'][1:]))
for T in theta:zero(T*dec(wh['projectors'][0]))
V=dec(packed(CAL/'canonical_so10_vector_quartic_ir_matching/primary_tables.json.gz')['light_embedding']);zero(V.T*V-s.eye(12))
ad=[s.SparseMatrix(45,45,{}) for _ in range(45)]
for a,b,c,z in bf['f']:ad[a][c,b]=s.sympify(z)
ah=[tidy(sum((V[a,h]*ad[a] for a in range(45) if V[a,h]),s.zeros(45))) for h in range(12)]
charges=[];alph=[]
for P in Pr:
    images=[tidy(T*P) for T in ah];dicts=[A.todok() for A in images]
    B=s.SparseMatrix(12,12,{(h,k):clean(sum(s.conjugate(z)*dicts[k].get(key,0) for key,z in dicts[h].items())) for h in range(12) for k in range(12)})
    charges.append(tidy(B));rank=s.trace(P);ar=[]
    for T in theta:
        a=clean(s.trace(P*T)/rank);zero(P*T-a*P);ar.append(a)
    alph.append(ar)
cp=s.Matrix([clean(sum(s.trace(P*theta[j]) for P in Pr)/(2*metric[j,j])) for j in range(3)])
ct=s.Matrix([clean(sum(s.trace(P*theta[j])*(L-U-s.log(lam/60)) for P,lam in zip(Pr,lams))/(2*metric[j,j])) for j in range(3)])
NF=[tidy(-sum((ar[j]*B/lam**2 for ar,B,lam in zip(alph,charges,lams)),s.zeros(12))/(24*metric[j,j])) for j in range(3)]
# Gauge-fixing source normalization is derived before eliminating b.
r,ss,bb,bc=s.symbols('r s b barc');psi=bc*(r+s.sqrt(x1*x2)*ss-x1*bb/2)
q1=s.diff(psi,x1).subs({x1:1,x2:1}).subs(bb,r+ss).expand();q2=s.diff(psi,x2).subs({x1:1,x2:1}).expand()
assert q1==-bc*r/2 and q2==bc*ss/2
assert s.diff(psi,x1).subs({x1:1,x2:1,bb:0}).expand()!=q1
# Exterior signs for the actual chi,K,c,barc source ordering.
def product(mask1,mask2):
    assert not(mask1&mask2)
    return (-1)**sum(i>j for i in range(4) if mask1&(1<<i) for j in range(4) if mask2&(1<<j))
sk_schi=-s.Rational(1,2)*product((1<<1)|(1<<2),(1<<0)|(1<<3))
gamma_chiK_rhoO=-sk_schi;gamma_chiK_S=-gamma_chiK_rhoO
Csign=-gamma_chiK_S # left K derivative crosses chi, then left chi derivative
assert Csign==s.Rational(1,2)
gp=packed(CAL/'canonical_so10_nine_family_uv_assembly/primary_tables.json.gz');finite={}
assert all(s.sympify(z)==0 for z in gp['pole_assembly']['finite_L_squared_coefficient_inside_g2'])
for key,gg in [('1/2',mp.mpf('.5')),('1',mp.mpf(1))]:
    family=gp['finite_cases'][key]['family_L_polynomials'];assert set(family)==set(FAMILIES)
    vals=[]
    for i in range(3):
        line=[]
        for k,name in enumerate(['constant','scale_log']):
            graph=mp.fsum(mp.mpf(family[f][i][k]) for f in FAMILIES)
            bridge=mp.fsum(gg**(p//2)*(mp.mpf(hr['coefficients'][str(p)][name][i])+ (mp.mpf(hr['coefficients'][str(p)]['coupling_log'][i])*mp.log(gg) if k==0 else 0)) for p in [-2,0,2,4])
            line.append(fmt(graph+bridge))
        assert all(s.Rational(family[f][i][2])==0 for f in FAMILIES if f not in ['VVVV','VVV'])
        quad=mp.fsum(mp.mpf(family[f][i][2]) for f in FAMILIES)
        assert abs(quad)<mp.mpf('1e-28')*(1+mp.fsum(abs(mp.mpf(family[f][i][2])) for f in FAMILIES))
        vals.append(line+['0'])
    finite[key]=vals
save('primary',{'method':'ordered_T_source_and_adjoint_images_explicit_family_sum','theta':list(map(enc,theta)),
    'charges':list(map(enc,charges)),'sector_alpha':[[str(z) for z in row] for row in alph],
    'C_t_pole_over_g2':list(map(str,cp)),'C_t_finite_over_g2':list(map(str,ct)),'C_F2':list(map(enc,NF)),
    'first_width_radial_source_zero_positions':432,'second_width_curvature_positions':432,
    'source_left_derivative_coefficient':str(Csign),'auxiliary_source_polynomials':[str(q1),str(q2)],
    'finite_lambda2_fixed_xi':finite,'finite_C1_calculated':False,'full_two_loop_width_identity_qualified':False,
    'physical_target_read':False},started)
