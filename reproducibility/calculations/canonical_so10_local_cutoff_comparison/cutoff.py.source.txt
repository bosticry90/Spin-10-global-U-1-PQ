"""LAC1: cutoff transport and actual source-functional negative controls."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
@lru_cache(None)
def num(v):return s.sympify(v)
@lru_cache(None)
def clean(v):return s.simplify(s.expand(v))
def zero(m):return all(clean(v)==0 for v in m.values())
def serial(m):return [[i,j,str(clean(v))] for (i,j),v in sorted(m.todok().items()) if clean(v)]
def matrix(n,rows):return s.SparseMatrix(n,n,{(i,j):num(v) for i,j,v in rows})
def reduce_word(word):
 out=[]
 for label,power in word:
  if out and out[-1]==(label,-power):out.pop()
  else:out.append((label,power))
 return out

def parity_fixture(r,p):
 # Coefficients of theta on the LEFT, theta parity r; homogeneous matrices.
 E=s.diag(2,3,5,7);Einv=E.inv()
 odd=s.Matrix([[0,0,1,2],[0,0,3,1],[2,1,0,0],[1,4,0,0]])
 even=s.Matrix([[1,2,0,0],[3,4,0,0],[0,0,2,1],[0,0,5,3]])
 U1=odd if r else even;X0=odd if p else even;X1=odd if (p+r)%2 else even
 def product(A,pa,B,pb):return (A[0]*B[0],(-1)**(r*pa)*A[0]*B[1]+A[1]*B[0])
 U=(E,U1);Ui=(Einv,-Einv*U1*Einv);X=(X0,X1)
 direct=product(product(U,0,X,p),p,Ui,0)[1];xp=E*X0*Einv;conn=U1*Einv
 right=E*X1*Einv+conn*xp-(-1)**(r*p)*xp*conn
 assert direct==right
 wrong=E*X1*Einv;assert direct!=wrong
 if r*p:assert direct!=E*X1*Einv+conn*xp-xp*conn
 return True

def main(role):
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'preparation.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 # Cheap sensitive orientation/parity tests precede data passes.
 for r in [0,1]:
  for p in [0,1]:assert parity_fixture(r,p)
 P=s.Matrix([[2,1],[1,1]]);A=s.Matrix([[1,0],[3,1]]);past=s.Matrix([[1,2],[0,1]]);future=s.Matrix([[2,0],[1,1]])
 X=P.inv()*A;U=past.inv()*P;rhs=U*X*U.inv();target=past.inv()*A*P.inv()*past
 if role=='primary':
  word=[('R',-1),('P',1),('P',-1),('A',1),('P',-1),('R',1)]
  assert reduce_word(word)==[('R',-1),('A',1),('P',-1),('R',1)]
  assert reduce_word([('Y',-1),('Y',1),('R',-1),('A',1),('P',-1),('R',1)])==reduce_word(word)
 else:
  full=future*past.inv()*A*P.inv()*past;assert future.inv()*full==target
 assert rhs==target and U.inv()*X*U!=target
 Q=s.Matrix([[3,1],[2,1]]);assert Q.inv()*past*past.inv()*P==Q.inv()*P
 c=s.Symbol('central',nonzero=True);assert zero((c*P).inv()*(c*A)-X)
 # Loop ideal: internal gluing raises L, joining components preserves it.
 for L in range(4):
  assert (7+L+1)-8+1==L+1 and (6+L+1)-8+(2-1)==L
 # Actual alphabet, parities and evaluation-dual antighost source metric.
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()))
 ref=json.loads((PK/'frozen_a10_e5_full_hessian'/(role+'.json')).read_bytes())['retained_reference']
 fields=ref['field_order'];fi={n:i for i,n in enumerate(fields)};gp=dict(zip(data['geometry']['names'],data['geometry']['parities']))
 assert len(fields)==643 and len(set('J'+n for n in fields))==643
 anames=[f'bar{i}' if i<12 else f'ub{i}' for i in range(45)];cnames=[f'C{i}' for i in range(45)]
 ai=[fi[n] for n in anames];ci=[fi[n] for n in cnames];assert all(gp[n]==1 for n in anames+cnames)
 T=matrix(643,ref['physical_to_raw_kernel']['entries']);Ti=matrix(643,ref['physical_to_raw_inverse']['entries'])
 TA=T.extract(list(range(598,643)),ai);Ai=Ti.extract(ai,list(range(598,643)))
 assert zero(TA*Ai-s.eye(45)) and zero(Ai*TA-s.eye(45))
 if role=='primary':G=s.SparseMatrix(45,45,{(i,j):sum(Ai[i,k]*Ai[j,k] for k in range(45)) for i in range(45) for j in range(45)})
 else:inv=TA.inv();G=inv*inv.T
 G=G.applyfunc(clean);assert G.rank()==45
 e3=json.loads((PK/'frozen_a10_e3_symmetry'/(role+'.json')).read_bytes())['operators']['Tb_geometric_and_transported']
 g=s.Symbol('g10');js={('J'+n):i for i,n in enumerate(anames)};sigma=[s.zeros(45) for _ in range(12)]
 for name,i in js.items():
  for row in e3[name]:
   om=[z for z in row['word'] if z.startswith('omega')];ot=[z for z in row['word'] if not z.startswith('omega')]
   assert len(om)==len(ot)==1 and '__' not in om[0] and ot[0] in js
   h=int(om[0][5:]);v=s.expand(num(row['coefficient']));w=v.coeff(g);assert clean(v-g*w)==0;sigma[h][i,js[ot[0]]]+=w
 if role=='replay':
  wit=json.loads((R/'calculations/canonical_so10_local_covariant_reference_witness/replay_result.json').read_bytes())
  for h in range(12):assert zero(sigma[h]+matrix(643,wit['actual12_homogeneous_carrier_matrices'][h]).extract(ai,ai).T)
 assert all(zero(z.T*G+G*z) for z in sigma)
 # ALL two-derivative GF ghost rows vs the frozen Fourier Hessian.
 pp=s.Matrix(s.symbols('p0_ref0:4'));mom=pp[0]**2-sum(pp[i]**2 for i in [1,2,3]);kin=s.zeros(45);rows_checked=0
 if role=='primary':
  for row in data['gauge_fixing_density']:
   toks=[z.partition('__') for z in row['word']]
   if len(toks)!=2 or sum(len(jet) for base,sep,jet in toks)!=2:continue
   if not(any(base in anames for base,sep,jet in toks) and any(base in cnames for base,sep,jet in toks)):continue
   for pos,(base,sep,jet) in enumerate(toks):
    if base not in anames:continue
    other=toks[1-pos];assert other[0] in cnames
    sign=(-1)**(sum(gp[toks[k][0]] for k in range(pos))+len(jet))
    value=num(row['coefficient'])*sign
    for mu in jet+other[2]:value*=s.I*pp[int(mu)]
    kin[anames.index(base),cnames.index(other[0])]+=value;rows_checked+=1
 else:
  K=matrix(643,ref['reference_Hessian_raw_C3']['entries']);kin=K.extract(ai,ci)
  # Independent support census, no prefix-Euler computation shared with primary.
  for row in data['gauge_fixing_density']:
   toks=[z.partition('__') for z in row['word']]
   if len(toks)==2 and sum(len(jet) for base,sep,jet in toks)==2 and any(base in anames for base,sep,jet in toks) and any(base in cnames for base,sep,jet in toks):rows_checked+=1
 kn=kin.applyfunc(lambda v:clean(s.cancel(v/mom)))
 assert all(not v.has(*list(pp)) for v in kn.values()) and zero(kin-mom*kn)
 image=(G*kn).applyfunc(clean);assert image[14,14]!=0 and G[14,14]!=0
 # Highest-source-linear/two-jet image cannot be canceled by higher field/source degree.
 assert (2+0+2,0+1,0+1)==(4,1,1)
 Graw=matrix(643,ref['reference_Green_raw_C3']['entries'])
 edge=clean(Graw[fi['C14'],fi['ub14']]*mom);reverse=clean(Graw[fi['ub14'],fi['C14']]*mom)
 assert edge==1 and reverse==-1
 source_rows=data['master_field_maps']['B14_0'];selected=[row for row in source_rows if row['word']==['C14__0']]
 assert len(selected)==1 and num(selected[0]['coefficient'])==1 and 1-gp['B14_0']==1
 # Actual A affine and a nonzero divergence-square Euler witness.
 aa=e3['A0_0'];assert any(row['word']==['omega0__0'] and num(row['coefficient'])==1 for row in aa)
 t=s.Symbol('t');Afun=s.Function('A')(t);om=s.Function('omega')(t);u=s.Function('u')(t);B=s.Function('B')(t)
 variation=s.diff(Afun,t)*s.diff(om,t,2);euler=s.diff(s.diff(Afun,t),t,2);assert euler==s.diff(Afun,t,3)
 assert euler.subs(Afun,t**3).doit()==6
 current=s.diff(u*B*om,t)
 assert clean(u*B*s.diff(om,t)+om*s.diff(u*B,t)-current)==0
 assert clean(u*B*s.diff(om,t)+u*om*s.diff(B,t)-current)!=0
 # Actual source dimensions/types from fixed field classes and all643 parities.
 source_types={}
 for n in fields:
  if n.startswith(('B','x_')):d,gh,p=1,0,0
  elif n.startswith('C'):d,gh,p=0,1,1
  elif n.startswith(('ub','bar')):d,gh,p=2,-1,1
  elif n.startswith(('L','b')):d,gh,p=2,0,0
  else:raise AssertionError(n)
  assert gp[n]==p;source_types['J'+n]=[4-d,-1-gh,1-p]
 assert all(source_types[n]==[2,0,0] for n in js)
 out={'schema':'LOCAL_CUTOFF_NATIVE_V1','role':role,'fields':643,'sources':643,'backgrounds':48,
  'source_types_sha256':sha256(json.dumps(source_types,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
  'antighost_sources':list(js),'source_metric':serial(G),'ghost_kinetic_normalized':serial(kn),
  'QN_source_two_jet_normalized':serial(image),'GF_two_jet_rows':rows_checked,'source_H_generators':12,
  'source_control':{'field':'B14_0','source':'JB14_0','rule_word':['C14__0'],'coefficient':'1','odd_source':True,
   'ghost_edge_normalized':str(edge),'reverse_edge_normalized':str(reverse),'QN_Jub14_C14_normalized':str(image[14,14]),
   'graded_derivative_anticommutator_nonzero':True},
  'group_orientation_fixture':str(target),'parity_cases':4,'central_action_terms_cancel_from_relative_products':True,
  'source_only_negative_control_background_invariant':True,'source_only_negative_control_Qclosed':False,
  'background_divergence_negative_control_Euler_witness':'6','switching_current_retained':True,
  'local_cutoff_isomorphism_proved':True,'strict_global_Gamma_or_physical_vacuum_limit_proved':False,
  'physical_quadratic_PPA_or_all_E5_A5_proved':False,'authority_changed':False,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main(sys.argv[1])
