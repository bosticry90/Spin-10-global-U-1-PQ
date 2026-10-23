"""SRG1 separate rational-field matrix validation and finite-scale comparison."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import gzip,json,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
spec=importlib.util.spec_from_file_location('srg_rational',CAL/'canonical_so10_light_pole_reduction/verify.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
point=read(CAL/'canonical_so10_positive_higgs/POINT.json')['determinant_polynomial'];aa=F(point['A'])
q.QB={0:F(point['B0'])/aa,6:F(point['B1'])/aa};q.QC={0:F(point['C0'])/aa,6:F(point['C1'])/aa}
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
fc=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz')
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_tables.json.gz')
M=q.decode(ht['raw_Hessian']);Mi=q.decode(ht['raw_Hessian_inverse']);assert q.mm(M,Mi)=={(i,i):{0:F(1)} for i in range(3)}
mp.mp.dps=90
av=mp.mpf(point['A']);bv=mp.mpf(point['B0'])+mp.mpf(point['B1'])*mp.sqrt(15);cv=mp.mpf(point['C0'])+mp.mpf(point['C1'])*mp.sqrt(15)
lo,hi=mp.mpf('.00530'),mp.mpf('.00531')
for _ in range(400):
    mid=(lo+hi)/2
    if av*mid*mid+bv*mid+cv>0:hi=mid
    else:lo=mid
root=(lo+hi)/2
def nm(matrix,n):return mp.matrix([[q.numeric(matrix.get((i,j),{}),root) for j in range(n)] for i in range(n)])
def trace(X):return sum((X[i,i] for i in range(X.rows)),mp.mpc(0))
def invchol(X):
    n=X.rows;L=mp.zeros(n)
    for i in range(n):
        for j in range(i+1):
            z=X[i,j]-sum((L[i,k]*mp.conj(L[j,k]) for k in range(j)),mp.mpc(0))
            if i==j:assert abs(mp.im(z))<mp.mpf('1e-65') and mp.re(z)>0;L[i,j]=mp.sqrt(mp.re(z))
            else:L[i,j]=z/L[j,j]
    inv=mp.zeros(n)
    for col in range(n):
        y=[mp.mpc(0)]*n;x=[mp.mpc(0)]*n
        for i in range(n):y[i]=((1 if i==col else 0)-sum((L[i,k]*y[k] for k in range(i)),mp.mpc(0)))/L[i,i]
        for i in reversed(range(n)):x[i]=(y[i]-sum((mp.conj(L[k,i])*x[k] for k in range(i+1,n)),mp.mpc(0)))/L[i,i]
        for i in range(n):inv[i,col]=x[i]
    return inv
W={p:mp.zeros(3,1) for p in [0,2,4]};positions=0;gold=0;mixed=0;wrong_reference=0;wrong_endpoint=0
sq=packed(CAL/'canonical_so10_scalar_quadratic_pullback/primary_tables.json.gz')
for row,peer,b in zip(A['stationary_operators'],B['stationary_operators'],fc['blocks']):
    assert row['block']==peer['block']==b['block'];n=b['multiplicity'];positions+=n*n
    P=q.decode(b['physical']);Pg=q.decode(b['gauge']);H=q.decode(b['H']);N=q.decode(b['N0'])
    hn=nm(q.ma(H,q.ms(N,{0:F(60)})),n);inv=invchol(hn);pn=nm(P,n)
    a,b2,l,y=b['label'];d3=F((a+1)*(b2+1)*(a+b2+2),2);d2=l+1;c3=F(a*a+b2*b2+a*b2+3*a+3*b2,3)
    beta=[F(3,5)*F(y,6)**2*d3*d2/6,F(d2*(d2*d2-1),12)*d3/6,d3*c3*d2/48]
    for k,(p,jet,other) in enumerate(zip([0,2,4],row['stationary_pole_jets'],peer['stationary_pole_jets'])):
        E=q.decode(jet);assert E==q.decode(other)
        assert not q.mm(q.mm(Pg,E),Pg);gold+=n*n;mixed+=len(q.mm(E,Pg))
        wrong_reference+=len(q.mm(q.mm(Pg,q.decode(b['P'][k])),Pg))
        if p==2:
            old=sq['blocks']['Htotal'][row['block']]
            changed={'shape':old['shape'],'entries':[[i,j,str(s.sympify(z,locals={'xi':s.Symbol('xi',real=True)}).subs(s.Symbol('xi',real=True),1))] for i,j,z in old['entries']]}
            wrong_endpoint+=len(q.ma(E,q.ms(q.decode(changed),{0:F(-1)})))
        tr=trace(pn*inv*nm(E,n));assert abs(mp.im(tr))<mp.mpf('1e-60')*(1+abs(tr))
        for i in range(3):W[p][i]+=mp.mpf((6*beta[i]).numerator)/(6*beta[i]).denominator*mp.re(tr)
assert positions==177 and gold==531 and mixed>0 and wrong_reference>0 and wrong_endpoint>0
halfghost=[]
for p in [0,2,4]:
    for i in range(3):
        frac=[q.numeric(q.expr(z),root) for z in A['stationary_vector_fractional_pole_jets'][str(p)]]
        vpart=sum(mp.mpf(F(fc['vector_indices'][r][i]).numerator)/F(fc['vector_indices'][r][i]).denominator*frac[r] for r in range(4))
        W[p][i]-=21*vpart
        if p==2:halfghost.append(vpart)
assert max(abs(z) for z in halfghost)>1
err=mp.mpf(0)
for p in [0,2,4]:
    for i in range(3):
        for native in [A,B]:
            z=abs(W[p][i]-mp.mpf(native['W_coefficients'][str(p)][i]))/(1+abs(W[p][i]));err=max(err,z);assert z<mp.mpf('1e-35')
assert A['W_coefficients']['-2']==B['W_coefficients']['-2']==['0']*3
assert A['parameter_directions']==34 and A['parameter_monomials']==342 and B['inverse_g2_cancellation_proved_exactly']
for native in [A,B]:assert native['finite_slope_read'] is native['new_parameter_beta_obtained_from_finite_slope'] is native['numerical_C1_calculated'] is False
# Bare scaling derives the factor2 for dimensionful and dimensionless inputs.
ep,d,E,Acoef,beta=s.symbols('eps d E A beta')
assert s.solve(beta+d*Acoef-E,s.Symbol('beta'))==[E-d*Acoef]
assert s.expand((E-d*Acoef).subs(E,(d+2)*Acoef)-2*Acoef)==0
for dimension_degree in [0,1,2]:
    assert s.expand((E-d*Acoef).subs({E:(dimension_degree+2)*Acoef,d:dimension_degree})-Acoef)==Acoef
# Independent formal Laurent grading identity for the COMPLETE sum.
e,L,b2,b1,b0,c2,c1,c0=s.symbols('e L b2 b1 b0 c2 c1 c0')
raw=(b2/e**2+b1/e+b0)*(1+2*e*L+2*e**2*L**2)+(c2/e**2+c1/e+c0)*(1+e*L+e**2*L**2/2)
sol=s.solve([b2+c2,2*b2+c2/2],[b2,c2]);assert sol=={b2:0,c2:0}
finite=s.expand(raw).coeff(e,0).subs(sol)
assert s.diff(finite,L)==2*(b1+c1)-c1
assert s.diff(finite,L)-(2*(b1+c1))==-c1
# Scalar Goldstone compression needs no extra raw metric. Test a literal
# raw/canonical congruence of this actual radial Hessian and its inverse.
mm=nm(M,3);S=mp.diag([mp.sqrt(60),mp.sqrt(mp.mpf(3)/5),mp.sqrt(mp.mpf(3)/5)]);si=S**-1
t=mp.matrix([1,2,3]);ar=mp.lu_solve(mm,-t);ac=mp.lu_solve(si*mm*si,-si*t)
assert max(abs(z) for z in si*ac-ar)<mp.mpf('1e-65')
assert max(abs(z) for z in mp.lu_solve(mm,-si*t)-ar)>mp.mpf('.01')
# Independent quantum inputs, inspected only after W is completed.
gp=packed(CAL/'canonical_so10_nine_family_uv_assembly/primary_tables.json.gz')
hr=read(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_result.json')
fr=read(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_result.json')
gs=packed(CAL/'canonical_so10_two_loop_gauge_beta/primary_tables.json.gz')
dc=[F(z)-F(gs['parent_c_two']) for z in gs['light_c_two_equal_g_row_sum']]
cases=[];passes=True;maxscale=mp.mpf(0);controls=[]
for key,gg in [('1/2',mp.mpf('.5')),('1',mp.mpf(1))]:
    vv=mp.matrix([sum(mp.mpf(A['W_coefficients'][str(p)][i])*gg**(p//2) for p in [-2,0,2,4]) for i in range(3)])
    BL=mp.matrix([sum(mp.mpf(hr['coefficients'][str(p)]['scale_log'][i])*gg**(p//2) for p in [-2,0,2,4]) for i in range(3)])
    FP=mp.matrix([sum(mp.mpf(fr['coefficients'][str(p)]['pole'][i])*gg**(p//2) for p in [-2,0,2,4]) for i in range(3)])
    GL=mp.matrix(gp['finite_cases'][key]['known_graph_local_scale_linear'])
    target=mp.matrix([6*gg*mp.mpf(z.numerator)/z.denominator for z in dc])
    defect=2*(GL+BL)+vv-target
    for i in range(3):
        z=abs(defect[i])/(1+abs(target[i]));maxscale=max(maxscale,z);passes=passes and z<mp.mpf('1e-28')
        assert abs(vv[i]-2*(FP[i]-BL[i]))<mp.mpf('1e-35')*(1+abs(vv[i]))
    assert max(abs(z) for z in 2*(GL+2*BL)+vv-target)>1
    assert max(abs(z) for z in 2*GL+vv-target)>1
    assert max(abs(z) for z in vv+2*BL)>1 # dropped full pole response is detectable
    cases.append({'g2':key,'W':list(map(lambda z:mp.nstr(z,50),vv)),
        'scale_defect':list(map(lambda z:mp.nstr(z,50),defect))})
out={'schema':'SRG1_VALIDATION_RECEIPT','status':'QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_AND_SCOPED_SCALE_IDENTITY' if passes else 'QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_WITH_FINITE_SCALE_MISMATCH',
    'execution_state':'COMPLETED','parameter_directions':34,'parameter_monomials':342,'complete_matrix_slots':177,
    'exact_goldstone_compression_positions':531,'mixed_orbit_columns_nonzero':mixed,
    'W_coefficients':A['W_coefficients'],'native_and_Cholesky_scaled_error':mp.nstr(err,15),'native_tolerance':'1e-35',
    'controls':{'reference_motion_instead_of_stationarity_changed_positions':wrong_reference,
    'endpoint_contamination_changed_positions':wrong_endpoint,'nonzero_Goldstone_pole_removed_only_after_exact_identity':True,
    'wrong_raw_metric_detected':True,'wrong_full_ghost_instead_of_half_detected':True,
    'wrong_dimensionful_pole_to_beta_factor_detected':True,'missing_forest_pole_detected':True,'double_bridge_detected':True},
    'scale_cases':cases,'scale_pass':bool(passes),'scale_maximum_scaled_defect':mp.nstr(maxscale,15),'scale_tolerance':'1e-28',
    'all_coupling_scale_statement':'STRUCTURAL_HOMOGENEITY_AND_QUALIFIED_FOREST_PREMISES;TWO_NUMERICAL_CASES_ARE_CORROBORATION',
    'numerical_C1_calculated':False,'full_original_C1_gate_qualified':False,'scientific_acceptance':'NOT_PERFORMED',
    'scientific_authority':'34/39_UNCHANGED','elapsed_after_imports':time.perf_counter()-started}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
