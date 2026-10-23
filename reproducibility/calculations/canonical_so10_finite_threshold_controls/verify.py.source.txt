"""FCT1 comparison and independent finite normalization/degeneracy controls."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
mp.mp.dps=85;A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
def compare(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:compare(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):compare(x,y)
    elif isinstance(a,str):
        try:x=mp.mpf(a);y=mp.mpf(b)
        except ValueError:assert a==b;return
        assert abs(x-y)<mp.mpf('1e-45')*(1+abs(x)),(a,b)
    else:assert a==b
compare(A,B)
assert A['basis']['finite_tensors']==4
assert A['basis']['charge_grams']==4 and len(A['basis']['wrong_transpose_nonzero_positions'])==3
assert all(x>0 for x in A['basis']['wrong_transpose_nonzero_positions']) and A['basis']['heavy_bridge']
historical=read(CAL/'canonical_so10_matrix_threshold/scalar_matrix_log.json')['lambda_scalar_SM_order_1_2_3']
for x,y in zip(A['scalar_lambda1_L0'],historical):assert abs(mp.mpf(x)-y)<mp.mpf('1e-8')*(1+abs(y))
TS=list(map(s.Rational,A['scalar_indices']));TV=[sum(s.Rational(row[i]) for row in A['vector_indices']) for i in range(3)]
assert TS==[s.Rational(377,5),77,79] and TV==[8,6,5]
slopes=[(21*TV[i]-TS[i])/2 for i in range(3)];gslopes=[-s.Rational(21,2)*x for x in TV]
assert slopes==[s.Rational(463,10),s.Rational(49,2),13]
for gs,rows in A['lambda1'].items():
    for i in range(3):
        assert abs(mp.mpf(rows[1][i])-mp.mpf(rows[0][i])-mp.re(num(slopes[i]))*2/7)<mp.mpf('1e-60')
for gs in ['3/4','1']:
    for i in range(3):
        diff=mp.mpf(A['lambda1'][gs][0][i])-mp.mpf(A['lambda1']['1/2'][0][i])
        assert abs(diff-mp.re(num(gslopes[i]))*mp.log(mp.re(num(gs))*2))<mp.mpf('1e-60')
# Derive the finite heat constant from the D-dimensional pole coefficient.
e=s.symbols('e');heat=s.expand(((4-2*e)/12-2)/2+s.Rational(1,24)-s.Rational(1,12))
assert heat==-s.Rational(7,8)-e/12
assert -12*heat.coeff(e)==1 and 12*heat.subs(e,0)==-s.Rational(21,2)
assert [str(x) for x in TV]!=['0','0','0'] # omitting epsilon term misses a nonzero vector-index constant.
assert abs(mp.mpf(A['elementary'][0][0])-mp.mpf(1)/6)<mp.mpf('1e-60')
assert mp.mpf(A['elementary'][0][1])==0
assert abs(mp.mpf(A['cubic_units'][1][0])-(mp.mpf(A['cubic_units'][0][0])+mp.log(2)/6)/2)<mp.mpf('1e-60')
for row in A['cubic_units'][:2]:assert max(map(mp.mpf,row))-min(map(mp.mpf,row))<mp.mpf('1e-60')
for value in A['pseudothreshold'][1:]:assert abs(mp.mpf(value)-mp.mpf(A['pseudothreshold'][0]))<mp.mpf('1e-6')
# An exact two-state degeneracy retains full charge insertions.
C=s.Matrix([[s.Rational(14,5),s.I],[-s.I,1]]);V=s.Matrix([[1,2],[2,3]]);mass=s.S(2)
actual=s.trace(C*V*C*V)/mass**2;averaged=s.trace((s.trace(C)/2*s.eye(2))*V*(s.trace(C)/2*s.eye(2))*V)/mass**2
assert actual!=averaged
# Covariant inverse kernel cancellation, including the actual radial bridge.
T=s.Matrix([[1,s.I/3],[s.Rational(1,7),2]]);M=s.Matrix([[3,1],[1,5]]);Gp=(T.T*M*T).inv()
zero(T*Gp*T.T-M.inv())
families=['VVVV','VVSS','SSSS','VVV','VVS','VSS','SSS','ghostV','ghostS'];assert len(set(families))==9
out={'status':'QUALIFIED_FINITE_THRESHOLD_BASIS_COINCIDENCE_AND_ONE_LOOP_CONTROLS','schema':'FCT1_VALIDATION',
 'elapsed_after_imports':time.perf_counter()-start,'physical_scalar_directions':290,'excluded_null_directions':38,
 'basis_proof_families':families,'full_finite_tensor_controls':4,'charge_grams':4,'heavy_tadpole_bridge':True,
 'lambda1_L_slopes':list(map(str,slopes)),'lambda1_log_g2_slopes':list(map(str,gslopes)),
 'controls':['wrong transpose','unchanged metric','wrong radial conjugation','omitted finite heat constant','omitted kinetic contact','charge averaging at degeneracy'],
 'arbitrary_positive_g_one_loop':True,'arbitrary_g_two_loop_evaluator':False,'physical_C1_or_refit_performed':False,
 'derivation':'DERIVATION.md','scientific_acceptance':'NOT_PERFORMED','authority':'34/39','state_sha256':'d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
