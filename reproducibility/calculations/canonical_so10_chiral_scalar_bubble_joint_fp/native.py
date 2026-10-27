from pathlib import Path
from hashlib import sha256
import gzip,json,sys,time,threading,os,math,sympy as s,mpmath as mp
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];assert role in ['primary','replay']
for p,h in read(O/'preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==O and p.name.startswith('replay' if role=='primary' else'primary'):raise PermissionError('SBJ_PEER_DENIED')
  if p.parent.name.startswith('canonical_so10_') and p.parent.resolve()!=O and('tables'in p.name or 'receipt'in p.name):raise PermissionError('SBJ_OLD_TARGET_DENIED')
sys.addaudithook(guard)
e=s.Symbol('epsilon',real=True);l=2**e/(1-e);x=s.Symbol('x',positive=True)
if role=='primary':assert s.simplify(2*2**(e-1)/(1-e)-l)==0
else:assert s.simplify(2*s.integrate(x**(-e),(x,0,s.Rational(1,2)),conds='none')-l)==0
assert s.simplify(s.diff(s.exp(s.Symbol('v')*e)*l,e).subs(e,0))==s.Symbol('v')+s.log(2)+1
mp.mp.dps=100;fmt=lambda z:mp.nstr(z,75);rows=[]
def norm(e,mu):return mp.exp(mp.euler*e)*mu**e
def lower_moment(n,e):return 2*mp.fsum((-1)**k*math.comb(n,k)*mp.mpf('.5')**(k+1-e)/(k+1-e) for k in range(n+1))
def calc(e,c,q,mu):
 N=norm(e,mu);L=2**e/(1-e);ss=(-mp.expm1(e*(mp.euler+mp.log(2*c*mu))-mp.log(1-e))/e) if e else -mp.euler-mp.log(2*c*mu)-1;IDR=(N*q**(-e)*mp.gamma(e)*mp.beta(1-e,1-e)-1/e) if e else mp.log(mu/q)+2;tail=mp.mpf(0)
 if role=='primary':
  I=2*N*mp.quad(lambda x:(q*x*(1-x))**(-e)*mp.gammainc(e,c*q*(1-x),mp.inf),[0,mp.mpf('.5')]);IR=I-ss;RI=IR-IDR
 else:
  RI=-N*c**e*mp.fsum((-c*q)**n*lower_moment(n,e)/(mp.factorial(n)*(e+n)) for n in range(1,64));IR=IDR+RI;I=IR+ss;tail=abs(N*c**e)*(c*q)**64*L/(mp.factorial(64)*(e+64));assert tail<mp.mpf('1e-48')
 bound=N*q*c**(1+e)*L/(1+e);assert -mp.mpf('1e-75')<=RI<=bound+mp.mpf('1e-75');s0=-mp.euler-mp.log(2*c*mu)-1;tau=-e*mp.log(c*mu);psi=tau*mp.exp(-tau)
 return {'I':fmt(I),'S':fmt(ss),'I_ren_beta0_comparator':fmt(IR),'ID_ren_beta0_comparator':fmt(IDR),'remainder':fmt(RI),'uniform_bound':fmt(bound),'series_tail_bound':fmt(tail),'premature_e0_log_subtraction':fmt(s0),'endpoint_countermodel_psi':fmt(psi)}
for ee in ['0','0.05','0.2']:
 for z,q in [('0.01','0.5'),('0.2','2'),('1.5','5')]:
  ev,zv,qv=map(mp.mpf,[ee,z,q]);row=calc(ev,zv/qv,qv,mp.mpf('1.5'));row.update({'epsilon':ee,'cq':z,'q':q,'kind':'finite'});rows.append(row)
 print('STAGE SBJ '+role+' epsilon '+ee+' finite complete',flush=True)
for ee in ['0.1','0.05','0.025']:
 for a in ['0.5','1','2']:
  ev,av=map(mp.mpf,[ee,a]);row=calc(ev,mp.exp(-av/ev)/2,mp.mpf(2),mp.mpf('1.5'));row.update({'epsilon':ee,'a':a,'q':'2','kind':'path','psi_joint_limit':fmt(av*mp.exp(-av))});rows.append(row)
print('STAGE SBJ '+role+' all paths complete',flush=True)
out={'schema':'SBJ1_SCALAR_JOINT_FP','role':role,'lower_face_L':'2**epsilon/(1-epsilon)','S0':'-EulerGamma-log(2*c*muR2)-1','joint_limit':'log(muR2/q)+2+beta_fin','beta_fin_kept_symbolic_in_interpretation_numeric_tables_use_zero_comparator':True,'scalar_bubble_nonlocal_log_retained':True,'endpoint_countermodel_limits':['0','0','a*exp(-a)'],'new_physical_scheme_baseline_or_authority':False,'rows':rows};raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with(O/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'elapsed_after_imports':time.perf_counter()-tick,'packed_sha256':sha256(blob).hexdigest(),'raw_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True);timer.cancel()
