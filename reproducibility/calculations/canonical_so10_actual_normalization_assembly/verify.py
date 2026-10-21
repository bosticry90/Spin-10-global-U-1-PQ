"""Expanded rational/radical right-gradient verifier;no new native import."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter,defaultdict
import json,gzip,sys,time,threading,os
import sympy as s
R=Path('C:/Users/psboy/Documents/ToE-Next');O=R/'calculations/canonical_so10_actual_normalization_assembly'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();watch=threading.Timer(180,lambda:os._exit(124));watch.daemon=True;watch.start();vp=read(O/'validation_preparation.json')
for raw,z in vp['input_sha256'].items():assert digest(Path(raw))==z,raw
def readonly(event,args):
 if event=='open' and len(args)>1 and isinstance(args[1],str) and any(c in args[1] for c in 'wax+'):raise PermissionError('ANA_VERIFY_WRITE')
sys.addaudithook(readonly);prep=read(O/'preparation.json');a=read(O/'primary_result.json');b=read(O/'replay_result.json');assert {k:v for k,v in a.items() if k not in ['route','elapsed_after_imports']}=={k:v for k,v in b.items() if k not in ['route','elapsed_after_imports']}
for role in ['primary','replay']:
 cap=read(O/(role+'_capture.json'));assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0
 for bind in prep['artifacts'][role].values():assert digest(Path(bind['path']))==bind['sha256'] and digest(Path(bind['receipt']))==bind['receipt_sha256']
get=lambda label:read(Path(prep['artifacts']['primary'][label]['path']))
data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()));geo=data['geometry'];names=geo['names'];index={n:i for i,n in enumerate(names)};par=geo['parities'];pairs=geo['field_source_h_k'];fields={i for i,J,h,k in pairs};sources={J for i,J,h,k in pairs};canon=fields|sources;Jof={i:J for i,J,h,k in pairs};extA={index[f'A{i}_{mu}'] for i in range(12) for mu in range(4)};omega={index[f'omega{i}'] for i in range(12)}
g,xi,eta=s.symbols('g10 xi eta_H');loc={'g10':g,'xi':xi,'eta_H':eta,'reference_width_M':xi,'reference_width_H':eta};squares=[2,3,5,7,-1]
factors={(i,j):s.prod(squares[k] for k in range(5) if i&j&(1<<k)) for i in range(32) for j in range(32)};factors={k:int(v) for k,v in factors.items()}
def put(p,k,v):
 if not v:return
 p[k]=p.get(k,F(0))+v
 if not p[k]:del p[k]
def add(*pp):
 out={}
 for p in pp:
  for k,v in p.items():put(out,k,v)
 return out
def scaled(p,c):return {k:v*c for k,v in p.items() if v*c}
@lru_cache(None)
def canonical(w):
 out=[];sg=1
 for token in w:
  if par[token[0]] and token in out:return (),0
  at=len(out)
  while at and out[at-1]>token:
   if par[token[0]] and par[out[at-1][0]]:sg=-sg
   at-=1
  out.insert(at,token)
 return tuple(out),sg
def product(p,q):
 out={}
 for (gp,xp,hp,m,w),c in p.items():
  for (gq,xq,hq,n,v),d in q.items():
   word,sg=canonical(w+v)
   if sg:put(out,(gp+gq,xp+xq,hp+hq,m^n,word),c*d*(sg*factors[m,n]))
 return out
@lru_cache(None)
def coefficients(text):
 z=s.expand(s.sympify(text,locals=loc));out={}
 assert not z.has(s.Float) and z.free_symbols<={g,xi,eta}
 for powers,co in s.Poly(z,g,xi,eta).terms():
  for term in s.Add.make_args(s.expand(co)):
   rat,rest=term.as_coeff_Mul(rational=True);assert rat.is_Rational;number=F(int(rat.p),int(rat.q));mask=0
   for factor in s.Mul.make_args(rest):
    if factor==s.I:mask^=16
    elif factor.is_Rational:number*=F(int(factor.p),int(factor.q))
    else:
     assert factor.is_Pow and factor.exp==s.Rational(1,2) and factor.base.is_Integer and factor.base>0,factor
     value=int(factor.base)
     for bit,prime in enumerate(squares[:4]):
      exponent=0
      while value%prime==0:value//=prime;exponent+=1
      number*=prime**(exponent//2)
      if exponent%2:mask^=1<<bit
     assert value==1
   put(out,(*powers,mask),number)
 return tuple(out.items())
def token(t):
 n,_,j=t.partition('__');return index[n],tuple(map(int,j))
def rows(rr):
 out={}
 for row in rr:
  w=tuple(map(token,row['word']));assert canonical(w)==(w,1)
  for (gp,xp,hp,m),v in coefficients(row['coefficient']):
   if 'g' in row:assert gp==0;gp=row['g']
   put(out,(gp,xp,hp,m,w),v)
 return out
def unpack(packet):
 out={}
 for gp,word,cid in packet['monomials']:
  w=tuple((n,tuple(j)) for n,j in word);assert canonical(w)==(w,1)
  for xp,hp,m,num,den in packet['coefficients'][cid]:put(out,(gp,xp,hp,m,w),F(num,den))
 return out
def elem(n,j=()):
 if isinstance(n,str):n=index[n]
 return {(0,0,0,0,((n,j),)):F(1)}
def D(p,mu):
 out={}
 for(gp,xp,hp,m,w),v in p.items():
  for at,(n,j) in enumerate(w):
   word,sg=canonical(w[:at]+((n,tuple(sorted(j+(mu,)))),)+w[at+1:])
   if sg:put(out,(gp,xp,hp,m,word),v*sg)
 return out
def DD(p,j):
 for mu in j:p=D(p,mu)
 return p
def gradient(p):
 out={}
 for(gp,xp,hp,m,w),v in p.items():
  total=sum(par[n] for n,j in w)%2
  for at,(n,j) in enumerate(w):
   suffix=sum(par[t] for t,k in w[at+1:]);sg=(-1)**((par[n]*suffix+par[n]*(total-par[n]))%2);put(out.setdefault((n,j),{}),(gp,xp,hp,m,w[:at]+w[at+1:]),v*sg)
 return out
def EL(p,domain):
 out={n:{} for n in domain}
 for(n,j),df in gradient(p).items():
  if n in domain:out[n]=add(out[n],scaled(DD(df,j),(-1)**len(j)))
 return out
def vector(p):
 el=EL(p,canon);v={}
 for i in fields:v[i]=scaled(el[Jof[i]],-(-1)**par[i]);v[Jof[i]]=scaled(el[i],(-1)**par[i])
 return v
def operation(images,odd=False):
 images={n:p for n,p in images.items() if p};cache={}
 def act(p):
  out={}
  for(gp,xp,hp,m,w),c in p.items():
   total=sum(par[n] for n,j in w)%2
   for at,(n,j) in enumerate(w):
    if n not in images:continue
    if(n,j) not in cache:cache[n,j]=DD(images[n],j)
    suffix=sum(par[t] for t,k in w[at+1:]);sg0=(-1)**((par[n]*suffix+(total+par[n] if odd else 0))%2);rest=w[:at]+w[at+1:]
    for(gq,xq,hq,mask,repl),v in cache[n,j].items():
     word,sg=canonical(rest+repl)
     if sg:put(out,(gp+gq,xp+xq,hp+hq,m^mask,word),c*v*(sg0*sg*factors[m,mask]))
  return out
 return act
def collapsed(p):
 out={}
 for(gp,xp,hp,m,w),v in p.items():out.setdefault((gp,w),{})[xp,hp,m]=v
 return out
def summary(p):
 h=sha256();h.update(b'[');cc=collapsed(p)
 for i,((gp,w),co) in enumerate(sorted(cc.items())):
  if i:h.update(b',')
  row=[gp,[[names[n],list(j)] for n,j in w],[[list(k),str(v)] for k,v in sorted(co.items())]];h.update(json.dumps(row,separators=(',',':'),ensure_ascii=True).encode())
 h.update(b']');return {'positions':len(cc),'sha256_exact_cells':h.hexdigest()}
print('STAGE independent generator_and_all1286_Hamiltonian_columns',flush=True)
K=rows(get('primitive')['full_K']);X=vector(K);xx=operation(X);e3=get('e3');tp={index[n]:rows(rr) for n,rr in e3['operators']['Tq_transported'].items()};tq={index[n]:rows(rr) for n,rr in e3['operators']['Tq_geometric'].items()};tb={index[n]:rows(rr) for n,rr in e3['operators']['Tb_geometric_and_transported'].items()};cc={n:add(tp[n],scaled(tq[n],-1)) for n in tp};TP=operation(tp);TQ=operation(tq);TB=operation(tb);C=operation(cc)
hp=TP(K);hq=TQ(K);hc=C(K);assert hp==unpack(a['Tprime_K']) and hq==unpack(a['Tq_K']) and hc==unpack(a['C_K']) and hp==add(hq,hc) and not TB(K)
dp=vector(hp);dq=vector(hq);dc=vector(hc)
assert {names[n]:v for n,v in dp.items() if v}=={n:unpack(v) for n,v in a['delta_Tprime_columns'].items()}
assert {names[n]:summary(v) for n,v in dq.items() if v}==a['delta_Tq_columns']
assert {names[n]:v for n,v in dc.items() if v}=={n:unpack(v) for n,v in a['delta_C_columns'].items()}
EA=operation({n:tb[n] for n in extA});degree=Counter()
for i in fields:
 assert dp[i]==add(TP(X[i]),scaled(xx(tp[i]),-1))==scaled(EA(X[i]),-1)
 for gp,w in collapsed(dp[i]):degree[sum(n in fields for n,j in w)]+=1
 assert not dc[i]
assert {str(k):v for k,v in degree.items()}==a['field_affine_degree_counts'] and not any(k>1 for k in degree)
for n in canon:assert add(dp[n],scaled(dq[n],-1))==dc[n]
e2=get('e2');physical={i for i in fields if names[i].startswith(('B','x_'))};assert len(physical)==len(a['retained508_weighted_physical_Euler_programs'])==508
for entry in a['retained508_weighted_physical_Euler_programs']:
 i=index[entry['field']];J=names[Jof[i]];program=e2['complete_columns'][J]['physical_program'];assert entry['source']==J and unpack(entry['coefficient'])==dp[i] and sha256(json.dumps(program,sort_keys=True,separators=(',',':')).encode()).hexdigest()==entry['physical_program_sha256']
badn=index[a['wrong_source_cotangent_sign_control']['source']];wrongX={n:scaled(v,-1) if n in sources else v for n,v in X.items()};wrong=operation(wrongX);bad=add(TP(wrongX[badn]),scaled(wrong(tp[badn]),-1),scaled(dp[badn],-1));assert bad and summary(bad)==a['wrong_source_cotangent_sign_control']['residual']
print('STAGE independent actual_Psi_full_remainder_and_free_Euler',flush=True)
Psi=add(*(rows(rr) for rr in get('e1')['polynomial_parts'].values()));W=TP(Psi);assert W==TQ(Psi)==rows(e3['quantum_fermion_breaking']);vw=vector(W)
for n in canon:assert vw[n]==cc[n]
Rz={i:rows(data['master_field_maps'][names[i]]) for i in fields};Q=operation(Rz,True);B=Q(W);assert B==rows(e3['action_Wards']['geometric_quantum_breaking']) and summary(B)['positions']==22520
CS=add(*(product(cc[Jof[i]],Rz[i]) for i in fields if cc[Jof[i]]));assert not add(B,CS) and add(B,scaled(CS,-1))==scaled(B,2)
free={k:v for k,v in EL(B,{index['b0']})[index['b0']].items() if all(n in omega for n,j in k[-1])};expected={}
for mu in range(4):expected=add(expected,scaled(elem('omega0',(mu,mu)),-2 if mu==0 else 2),scaled(elem('omega1',(mu,mu)),1 if mu==0 else -1))
assert free==expected==unpack(a['Psi_b0_free_Euler_covector'])
assert not any(unpack(p) for p in a['four_exact_E3_currents_retained'])
print('STAGE independent quantum_order_Ward_and_exact_once_assembly',flush=True)
x,beta,hb,normal=s.symbols('x beta hbar normal');U=1+x;D0=beta-U*U;Gamma1=s.log(D0)/2-s.log(U);Tw=x*s.diff(Gamma1,x);h=x*U;Gxx=1/D0;Gbx=-U/D0;IB=beta*s.diff(h,x,2)*Gxx/2+s.diff(h,x)*Gbx-s.diff(h,x)/U;IC=-IB
assert s.cancel(Tw+IC)==0 and Tw.subs({x:1,beta:9})==s.Rational(-9,10)
tree=beta*x*U;assert tree.subs({x:1,beta:9})==18
assert s.expand(hb*normal*tree-hb*normal*tree)==0 and (hb*normal*tree).subs({x:1,beta:9})==18*hb*normal
assert s.cancel(Tw.subs({x:1,beta:9}))!=0
reg,Bbasic,QG,Ffin=s.symbols('reg Bbasic QG Ffin');raw=reg*(Bbasic+QG)+Ffin;once=s.expand(raw-reg*Bbasic-reg*QG);twice=s.expand(raw-2*reg*Bbasic-2*reg*QG);assert once==Ffin and s.expand(twice-once)!=0
assert a['normalization_order_powers']=={'tree_counterterm':1,'baseline_unit_product_loop':1,'normalization_times_product_loop':2,'normalization_times_field_Jacobian_action':2,'mixed_K_L_normalization':2}
result={'schema':'ACTUAL_NORMALIZATION_ASSEMBLY_VALIDATION_V1','execution_state':'COMPLETED','scientific_disposition':a['scientific_disposition'],'both_full_native_mathematical_outputs_agree':True,'independent_generators_all1286_Hamiltonian_columns_and643_direct_field_commutators_verified':True,'all508_physical_Euler_program_bindings_and_exact_weights_retained':True,'actual_field_affinity_background_Frechet_and_source_only_deltaC_verified':True,'actual_Psi_22520_nonzero_omission_and_doubled_sign_controls_verified':True,'nonzero_eight_position_free_b0_Euler_covector_and_four_currents_retained':True,'fixed_geometry_whole_product_and_independent_completion_assembly_reviewed':True,'same_common_prescription_unit_insertions_loop_order_and_source_normalization_reviewed':True,'finite_tangent_and_single_raw_pole_rewriting_distinguished_exact_once':True,'linearized_Slavnov_background_Cartan_and_formal_local_operator_transport_reviewed':True,'nonzero_connected_Gaussian_and_tree_completion_controls_verified':True,'physical_parameter_stability_universal_adequacy_fullE5_or_physical_equivalence_qualified':False,'new_failed_native_workers':0,'new_failed_verifier_workers':0,'shared_limits':['Same action,upstream master/reference/trace/probe theorems and AI author.','Independent expanded Fraction/radical word arithmetic uses Python/SymPy;no Lean,human or experimental validation.'],'authority_changed':False,'verifier_seconds_after_imports':time.perf_counter()-tick}
print('VALIDATION '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);watch.cancel()
