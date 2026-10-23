"""FAN1 separate rational tensor, source-width and finite-inventory checks."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import gzip,json,os,sys,threading,time,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation_v2.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
spec=importlib.util.spec_from_file_location('fan_rational',CAL/'canonical_so10_light_pole_reduction/verify.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_v2_tables.json.gz')
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_tables.json.gz');hr=read(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_result.json')
M=q.decode(ht['raw_Hessian']);Mi=q.decode(ht['raw_Hessian_inverse']);assert q.mm(M,Mi)=={(i,i):{0:F(1)} for i in range(3)}
for name in ['theta','charges','C_F2']:
    assert len(A[name])==len(B[name])
    for x,y in zip(A[name],B[name]):assert q.decode(x)==q.decode(y)
L,U=s.symbols('L U',real=True)
parse=lambda x:s.sympify(x,locals={'L':L,'U':U})
clean=lambda x:s.expand(s.radsimp(s.expand(x)))
for name in ['C_t_pole_over_g2','C_t_finite_over_g2']:
    assert len(A[name])==len(B[name])==3
    assert all(clean(parse(x)-parse(y))==0 for x,y in zip(A[name],B[name]))
cp=s.Matrix(list(map(parse,A['C_t_pole_over_g2'])));ct=s.Matrix(list(map(parse,A['C_t_finite_over_g2'])))
assert cp==s.Matrix([5,s.Rational(25,4),0])
mx=s.SparseMatrix(*ht['raw_Hessian']['shape'],{(i,j):s.sympify(z) for i,j,z in ht['raw_Hessian']['entries']})
lams=[s.Rational(3,10),s.Rational(3,2),s.Integer(25),s.Rational(253,10)]
gold=s.Matrix(ht['Goldstone_potential_radial_traces'])
dt=s.Matrix([sum(lam*gold[i,r]*(U+s.log(lam/60)-L)/2 for r,lam in enumerate(lams)) for i in range(3)])
assert (mx*ct+dt).applyfunc(clean)==s.zeros(3,1)
ut=read(CAL/'canonical_so10_uv_radial_tadpoles/primary_result.json')
assert (mx*cp-s.Matrix([s.sympify(z)/4 for z in ut['mixed_fractional_exact']])).applyfunc(clean)==s.zeros(3,1)
# Full 3x12x12 tensor is compared; the physical F2 tests use all3 probe ideals.
NF=[s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']}) for d in A['C_F2']]
probes=[0,1,4];Fproj=s.Matrix([[NF[j][h,h] for h in probes] for j in range(3)])
rm=s.SparseMatrix(*ht['Rminus2']['shape'],{(i,j):s.sympify(z) for i,j,z in ht['Rminus2']['entries']})
assert (12*mx*Fproj+rm.T).applyfunc(clean)==s.zeros(3)
for X in NF:assert (X-X.T).applyfunc(clean)==s.zeros(12)
# Nonzero neutral sector enters C_t but is invisible to its F2 curvature.
assert q.decode(A['charges'][1])=={} and any(parse(z)!=0 for z in A['sector_alpha'][1])
metric=list(map(s.Rational,['60','3/5','3/5']));ranks=[8,1,12,12]
neutral=s.Matrix([parse(A['sector_alpha'][1][j])*ranks[1]/(2*metric[j]) for j in range(3)])
assert neutral!=s.zeros(3,1)
assert (mx*(2*ct)+dt).applyfunc(clean)!=s.zeros(3,1)
assert (-mx*ct+dt).applyfunc(clean)!=s.zeros(3,1)
# A mass-sector charge average can preserve the source pole yet changes F2.
charges=[s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']}) for d in A['charges']]
wrong=charges.copy();wrong[0]=sum(charges[0][h,h] for h in probes)*s.eye(12)/3
bad=[-sum((parse(ar[j])*Q/lam**2 for ar,Q,lam in zip(A['sector_alpha'],wrong,lams)),s.zeros(12))/(24*metric[j]) for j in range(3)]
assert any((bad[j]-NF[j]).applyfunc(clean)!=s.zeros(12) for j in range(3))
# The bubble curvature kernel follows from both proper-time moments and
# mass differentiation; keep epsilon until a UV-finite coefficient is reached.
e,x=s.symbols('eps x',positive=True)
assert s.simplify(-s.diff(s.gamma(1+e)*x**(-1-e)/12,x)-s.gamma(2+e)*x**(-2-e)/12)==0
assert s.limit(s.gamma(2+e)*x**(-2-e)/12,e,0)==1/(12*x*x)
r,z,beta,bc=s.symbols('r z beta barc');q1=bc*(z/2-beta/2);q2=bc*z/2
assert s.expand(q1.subs(beta,r+z))==-bc*r/2
assert q2!=s.expand(q1.subs(beta,r+z))
assert s.Rational(A['source_left_derivative_coefficient'])==s.Rational(B['source_left_derivative_coefficient'])==s.Rational(1,2)
for data in [A,B]:
    assert data['first_width_radial_source_zero_positions']==data['second_width_curvature_positions']==432
    assert data['finite_C1_calculated'] is data['full_two_loop_width_identity_qualified'] is data['physical_target_read'] is False
# Algebraic inventory/forest transport, no assigned finite residue.
cfh,cfs,cph,cps,m,bridge=s.symbols('cfh cfs cph cps m bridge')
full=m+(cph+cps)-(cfh+cfs)+cfs-cps+bridge
assert s.expand(full-(m+cph-cfh+bridge))==0
assert s.expand(full.subs(cph,cfh)-(m+bridge))==0
# Field-origin finite allocation with actual M; use generic covectors.
av=s.Matrix(s.symbols('a0:3'));tv=s.Matrix(s.symbols('t0:3'));rv=s.Matrix(1,3,s.symbols('r0:3'))
assert (rv*av-rv*mx.inv()*(tv+mx*av)+rv*mx.inv()*tv).applyfunc(s.simplify)==s.zeros(1,1)
mp.mp.dps=90;maxerr=mp.mpf(0);positions=0
gp=packed(CAL/'canonical_so10_nine_family_uv_assembly/primary_tables.json.gz')
for key,gg in [('1/2',mp.mpf('.5')),('1',mp.mpf(1))]:
    for i in range(3):
        for k in range(3):
            aa=mp.mpf(A['finite_lambda2_fixed_xi'][key][i][k]);bb=mp.mpf(B['finite_lambda2_fixed_xi'][key][i][k])
            err=abs(aa-bb)/(1+abs(aa));maxerr=max(maxerr,err);assert err<mp.mpf('1e-28');positions+=1
        # Missing bridge and extra old FCI are sensitive mistakes at both cases.
        actual=mp.mpf(A['finite_lambda2_fixed_xi'][key][i][0]);old=mp.mpf(gp['finite_cases'][key]['known_graph_local_finite_L0'][i]);assert abs(actual-old)>1
# Conditional Nielsen/bridge relation in Gamma-to-Lambda normalization.
Ct=s.Matrix(s.symbols('c0:3'));CF=s.Matrix(s.symbols('f0:3'));R=s.Matrix(1,3,s.symbols('R0:3'));T=s.Matrix(s.symbols('T0:3'));g=s.Symbol('g',positive=True)
dR=12*(mx*CF).T/g**2;dT=-mx*Ct
variation1PI=-(R*Ct)[0]+12*(T.T*CF)[0]/g**2
variationBridge=-(dR*mx.inv()*T+R*mx.inv()*dT)[0]
assert s.simplify(variation1PI+variationBridge)==0
assert positions==18
out={'schema':'FAN1_VALIDATION_RECEIPT','status':'QUALIFIED_FIXED_XI_FINITE_BOSONIC_ASSEMBLY_AND_FIRST_NIELSEN_KERNEL',
    'execution_state':'COMPLETED','finite_coefficient_positions':18,'finite_assembly_scaled_error':mp.nstr(maxerr,15),'finite_assembly_tolerance':'1e-28',
    'radial_curvature_positions':432,'first_width_structural_zero_positions':432,'source_tadpole_log_positions':9,
    'source_curvature_probe_positions':9,'full_two_loop_width_identity_qualified':False,
    'conditional_width_cancellation_only':True,'finite_C1_calculated':False,
    'controls':{'missing_half_source_detected':True,'wrong_source_sign_detected':True,'omitted_auxiliary_term_detected':True,
    'charge_average_detected':True,'neutral_sector_F2_insensitive_but_tadpole_sensitive':True,'missing_bridge_detected':True},
    'scientific_acceptance':'NOT_PERFORMED','scientific_authority':'34/39_UNCHANGED','elapsed_after_imports':time.perf_counter()-started}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
