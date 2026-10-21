"""Independent full coefficient replay and algebra/counterterm checks."""
from pathlib import Path
from hashlib import sha256
from itertools import product,permutations
from functools import lru_cache
from collections import defaultdict
from fractions import Fraction
import json,gzip,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
@lru_cache(None)
def c(z):return s.cancel(s.expand(z))
@lru_cache(None)
def expr(z):return s.sympify(z)
def main():
 tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((D/'validation_preparation.json').read_bytes())
 for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
 aa=[json.loads((D/(r+'_result.json')).read_bytes()) for r in ['primary','replay']]
 data=json.loads((P/'frozen_a10_physical_reconciliation/full_replay.json').read_bytes())
 raw=[gzip.decompress((D/(r+'_tables.json.gz')).read_bytes()) for r in ['primary','replay']]
 assert raw[0]==raw[1]
 for r,a,rr in zip(['primary','replay'],aa,raw):
  assert sha256(rr).hexdigest()==a['table_sha256']
  assert sha256((D/(r+'_tables.json.gz')).read_bytes()).hexdigest()==a['table_compressed_sha256']
  assert not a['C1_GS_calculated'] and not a['authority_changed'] and a['H_generators_checked']==12
 tables=json.loads(raw[0]);T={(a,b,i):expr(z) for a,b,i,z in tables['T']}
 f={(a,b,k):expr(z) for a,b,k,z in tables['f']}
 orbit={(i,a):expr(z) for i,a,z in tables['orbit']};v={i:expr(z) for i,j,z in data['vacuum']['VEV']['entries']}
 # Independent coefficient-by-coefficient contraction over complete I,a,b.
 rep=[defaultdict(dict) for _ in range(45)];off=0
 for sector,n in [('Phi',54),('Sigma',252),('phi',20),('S',2)]:
  for a,row in enumerate(data['representation_matrices'][sector]):
   for i,j,z in row['entries']:rep[a][i+off][j+off]=expr(z)
  off+=n
 ov={};direct={};omitted_antisymmetric=0
 for a in range(45):
  for i in range(328):
   val=c(sum(z*v.get(j,0) for j,z in rep[a][i].items()))
   if val:ov[i,a]=val
 assert ov==orbit
 oi=defaultdict(list)
 for (j,a),z in ov.items():oi[a].append((j,z))
 for a,b in product(range(45),repeat=2):
  cand=defaultdict(lambda:s.S.Zero)
  for j,z in oi[a]:
   for i,t in rep[b][j].items():cand[i]+=z*t
  for i in range(328):
   val=c(cand[i]);assert val==T.get((a,b,i),0),(a,b,i)
   if val:direct[a,b,i]=val
 assert direct==T and len(direct)==aa[0]['tensor_nonzero']
 # Actual noncommuting ghost-index information, and known insensitive projection.
 residual={};symmetric={}
 for a,b,i in set(T)|{(b,a,i) for a,b,i in T}:
  z=c((T.get((a,b,i),0)+T.get((b,a,i),0))/2)
  if z:symmetric[a,b,i]=z
  z=c(T.get((a,b,i),0)-T.get((b,a,i),0))
  if z:residual[a,b,i]=z
 assert residual and symmetric!=T
 for a,b in product(range(45),repeat=2):
  assert c(sum(v[i]*(T.get((a,b,i),0)-symmetric.get((a,b,i),0)) for i in v))==0
 # Faithful 10-plane commutators independently validate all stored f entries.
 planes=[]
 for i in range(10):
  for j in range(i+1,10):
   h=s.zeros(10);h[i,j]=1/s.sqrt(2);h[j,i]=-1/s.sqrt(2);planes.append(h)
 for a,b in product(range(45),repeat=2):
  comm=planes[a]*planes[b]-planes[b]*planes[a]
  rhs=s.zeros(10)
  for k in range(45):
   if (a,b,k) in f:rhs+=f[a,b,k]*planes[k]
  assert (comm-rhs).applyfunc(c)==s.zeros(10)
 assert len(f)==720 and any(z!=2*z for z in f.values())
 print('STAGE independently_replayed_full_tensor',time.perf_counter()-tick,flush=True)
 # Enumerate valid species pairings independently of native inventory code.
 cubic=['SSS','SSV','SVV','VVV'];quartic=['SSSS','SSVV','VVVV']
 pairings_count={}
 for a in cubic:
  for b in cubic:
   valid=sum(all(a[i]==b[j] for i,j in enumerate(perm)) for perm in permutations(range(3)))
   if valid:pairings_count[a+b]=valid
 assert set(pairings_count)=={'SSSSSS','SSVSSV','SVVSVV','VVVVVV'}
 assert [pairings_count[k] for k in ['SSSSSS','SSVSSV','SVVSVV','VVVVVV']]==[6,2,2,6]
 catalog=tables['background_words'];counts={name:len(rows) for name,rows in catalog.items()}
 assert counts=={'VVVV':8,'VVSS':8,'SSSS':8,'VVV':29,'VVS':15,'VSS':29,'SSS':15,'ghostV':29,'ghostS':15,'one_loop_CT':6}
 # Different check of universal ordered inverse rule: exact 2x2 noncommuting
 # jets and direct differentiation of the inverse rational matrix.
 h,k=s.symbols('h k');K=s.diag(2,3);H=s.Matrix([[1,2],[0,-1]]);J=s.Matrix([[0,1],[3,2]]);S=s.Matrix([[2,0],[1,-2]])
 G=K.inv();target=(K+h*H+k*J+h*k*S).inv().diff(h).diff(k).subs({h:0,k:0})
 rule=G*H*G*J*G+G*J*G*H*G-G*S*G
 assert target==rule
 assert target!=rule+G*S*G and target!=rule-G*J*G*H*G
 # Evaluate EVERY stored placement against direct derivatives of an ordered
 # matrix product. This diagnostic is sensitive to omitted vertex derivatives.
 def baseG(n):return s.diag(2+n,3+n).inv()
 def kh(n,jet):
  if jet=='h':return H+n*s.eye(2)
  if jet=='k':return J-n*s.eye(2)
  return S+n*s.eye(2)
 def vertex(n,jet):
  if not jet:return s.Matrix([[1+n,2],[3,-1-n]])
  if jet=='h':return H+n*s.eye(2)
  if jet=='k':return J+n*s.eye(2)
  return S # CT only
 def jet(token):
  n,jj=token
  if n[0]=='G':return baseG(int(n[1:]))
  if n[0]=='K':return kh(int(n[1:]),jj)
  return vertex(0 if n=='CT' else int(n[1:]),jj)
 diagnostic={}
 for name,entries in catalog.items():
  assembled=s.zeros(2)
  for z,word in entries:
   term=s.eye(2)
   for token in word:term*=jet(token)
   assembled+=expr(z)*term
  edges=1 if name=='one_loop_CT' else 2 if name in ['VVVV','VVSS','SSSS'] else 3
  nv=1 if edges<3 else 2;vdegree=2 if name=='one_loop_CT' else int(name in ['VVV','VSS','ghostV'])
  # Independent product rule with matrix-valued jets, summing differentiated
  # slots; no import of the native word-derivative or insertion routines.
  slots=[]
  for n in range(edges):
   g0=baseG(n);hh=kh(n,'h');kk=kh(n,'k');ss=kh(n,'hk')
   slots.append((g0,-g0*hh*g0,-g0*kk*g0,g0*hh*g0*kk*g0+g0*kk*g0*hh*g0-g0*ss*g0))
  for n in range(nv):slots.append((vertex(n,''),vertex(n,'h') if vdegree else s.zeros(2),vertex(n,'k') if vdegree else s.zeros(2),S if vdegree==2 else s.zeros(2)))
  expected=s.zeros(2)
  for ii,jj in product(range(len(slots)),repeat=2):
   term=s.eye(2)
   for index,sl in enumerate(slots):term*=sl[3 if index==ii==jj else 1 if index==ii else 2 if index==jj else 0]
   expected+=term
  assert assembled==expected,name
  diagnostic[name]=[[str(v) for v in row] for row in expected.tolist()]
  if vdegree and name!='one_loop_CT':
   # Deleting all words with a vertex jet changes this actual diagnostic.
   incomplete=s.zeros(2)
   for z,word in entries:
    if any(n.startswith('V') and jj for n,jj in word):continue
    term=s.eye(2)
    for token in word:term*=jet(token)
    incomplete+=expr(z)*term
   assert incomplete!=assembled
 # Two-width and Legendre/tadpole distinctions; no CT coefficients chosen.
 x,y=s.symbols('x y',positive=True);E=s.sqrt(y/x)-1
 assert s.diff(E,x).subs({x:1,y:1})==-s.Rational(1,2)
 assert s.diff(E,y).subs({x:1,y:1})==s.Rational(1,2)
 assert (s.diff(E,x)+s.diff(E,y)).subs({x:1,y:1})==0 # equal-width control is blind
 t=s.symbols('t');K0=s.diag(2,3);delta=s.Matrix([[0,t],[t,0]])
 assert s.trace(K0.inv()*delta)==0
 # One-loop heat convention independently expanded before taking epsilon^0.
 e,L=s.symbols('e L');hv=(4-2*e)/24-1+s.Rational(1,24)-s.Rational(1,12)
 ren=s.expand(hv*(1/e-L)+s.Rational(7,8)/e)
 assert ren.subs(e,0)==7*L/8-s.Rational(1,12)
 # Full original parent/point remain authenticated; no finite vector exists.
 elapsed=time.perf_counter()-tick
 receipt={'schema':'C1_BACKGROUND_THRESHOLD_INPUT_VALIDATION_V1',
 'status':'PASS_BOUNDED_KINEMATIC_INPUT_AND_TOPOLOGY_ONLY','input_bindings':len(prep['input_sha256']),
 'full_T_positions_replayed':664200,'nonzero_T':len(T),'zero_complement':664200-len(T),
 'f_positions_checked':91125,'f_nonzero':720,'orbit_coefficients':len(orbit),
 'native_tables_identical':True,'whole_tensor_antisymmetric_control':True,
 'v_contraction_control_is_insensitive_to_antisymmetric_omission':True,
 'ordered_AA_words':156,'generic_CT_words':6,'independent_matrix_controls':diagnostic,
 'native_failures':0,'verifier_failures':0,'mass_VEV_tadpole_finite_CT_complete':False,
 'C1_GS_calculated':False,'complete_diagram_weighted_amplitude':False,
 'historical_A10_or_E1_action_adopted':False,'authority_changed':False,
 'state_sha256':sha256((R/'project_state.json').read_bytes()).hexdigest(),
 'formal_authority':'34/39_UNCHANGED','custody':'EXIT2_SEVEN_UNRESOLVED_NOT_RERUN',
 'shared_premises':'physical action, representation and VEV data, SymPy, published conventions, same AI author',
 'elapsed_after_imports':elapsed}
 print('RESULT '+json.dumps(receipt,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
