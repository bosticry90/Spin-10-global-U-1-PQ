"""Expanded rational/radical right-gradient verifier;no new native import."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter,defaultdict
import json,gzip,sys,time,threading,os
import sympy as s
R=Path('C:/Users/psboy/Documents/ToE-Next');O=R/'calculations/canonical_so10_physical_counterterm_span'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();watch=threading.Timer(180,lambda:os._exit(124));watch.daemon=True;watch.start();vp=read(O/'validation_preparation.json')
for raw,z in vp['input_sha256'].items():assert digest(Path(raw))==z,raw
def readonly(event,args):
 if event=='open' and len(args)>1 and isinstance(args[1],str) and any(c in args[1] for c in 'wax+'):raise PermissionError('PCS_VERIFY_WRITE')
sys.addaudithook(readonly);prep=read(O/'preparation_v2.json');a=read(O/'primary_v2_result.json');b=read(O/'replay_v2_result.json');assert {k:v for k,v in a.items() if k not in ['route','elapsed_after_imports']}=={k:v for k,v in b.items() if k not in ['route','elapsed_after_imports']}
for role in ['primary','replay']:
 cap=read(O/(role+'_v2_capture.json'));assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0
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
def mat(packet):
 m=s.zeros(*packet['shape'])
 for i,j,z in packet['entries']:m[i,j]=s.sympify(z)
 return m
def GD(p):return {key:c*key[0] for key,c in p.items() if key[0]}
def DG(p):
 out={}
 for(gp,xp,hp,m,w),v in p.items():
  if gp:put(out,(gp-1,xp,hp,m,w),v*gp)
 return out
def sparse_rank(rows):
 piv={}
 for original in rows:
  row=dict(original)
  while row:
   k=min(row)
   if k not in piv:
    lead=row[k];piv[k]={j:v/lead for j,v in row.items()};break
   factor=row[k]
   for j,v in piv[k].items():put(row,j,-factor*v)
 return len(piv)
print('STAGE independent complete_carriers_and_actual_independent_background_Ward',flush=True)
e1=get('e1');e2=get('e2');e3=get('e3');action=get('action');tp={index[n]:rows(rr) for n,rr in e3['operators']['Tq_transported'].items()};tb={index[n]:rows(rr) for n,rr in e3['operators']['Tb_geometric_and_transported'].items()};db={n:add(tb.get(n,{}),scaled(tp.get(n,{}),-1)) for n in fields|extA};DB=operation(db)
physical={i for i in fields if names[i].startswith(('B','x_'))};assert len(physical)==508 and all(not db[i] for i in physical) and all(db[i]==tb[i] for i in extA)
coarse=set()
for na in range(5):
 for nb in range(5-na):
  for nx in range(5-na-nb):
   count=na+nb+nx
   for nd in range(5-count):
    if (na+nb+nd)%2==0 and (count or not nd):coarse.add((na,nb,nx,nd,4-count-nd,na+nb+nd))
assert sorted(coarse)==[tuple(c) for c in a['raw_carrier_census']] and len(coarse)==36
# Every carrier has an explicit proof endpoint. This tests for omitted low-
# dimension B*dx and x*B^2 carriers rather than assuming only dimension4 words.
endpoints=Counter()
for na,nb,nx,nd,dim,rank in coarse:
 nv=na+nb
 if not nv:assert nd==0 or (nx,nd) in [(1,2),(2,2)];tag='scalar_potential_boundary_or_kinetic'
 elif not nx:assert (nv,nd) in [(1,1),(1,3),(2,0),(2,2),(3,1),(4,0)];tag='vector_Noether_or_independent_group_exclusion'
 else:assert (nv,nx,nd) in [(1,1,1),(2,1,0),(1,2,1),(2,2,0)];tag='scalar_connection_completion_or_mixed_exclusion'
 endpoints[tag]+=1
assert sum(endpoints.values())==36
print('STAGE independent rational_real_H_metric_constraint_elimination',flush=True)
rz={i:rows(data['master_field_maps'][names[i]]) for i in fields};Q=operation(rz,True);hids={index[f'C{i}']:i for i in range(12)};real=[[[F(0) for j in range(12)] for i in range(12)] for l in range(12)];imag=[[[F(0) for j in range(12)] for i in range(12)] for l in range(12)]
for target in range(12):
 for(gp,xp,hp,mask,w),v in rz[index[f'C{target}']].items():
  if all(n in hids for n,j in w):
   assert gp==1 and xp==hp==0 and mask in [1,17] and len(w)==2 and all(not j for n,j in w)
   b0,c0=[hids[n] for n,j in w];dst=imag if mask==17 else real;dst[b0][target][c0]-=v;dst[c0][target][b0]+=v
ad=[s.Matrix(12,12,lambda i,j:s.sqrt(2)*(s.Rational(real[l][i][j].numerator,real[l][i][j].denominator)+s.I*s.Rational(imag[l][i][j].numerator,imag[l][i][j].denominator))) for l in range(12)]
assert ad==[mat(packet) for packet in a['H_adjoint_matrices']]
import itertools
keys=list(itertools.combinations_with_replacement(range(12),2));ki={k:i for i,k in enumerate(keys)};eq=[]
for l in range(12):
 for i,j in keys:
  rr={};ii={}
  for k in range(12):
   for var,cr,ci in [(ki[tuple(sorted((k,j)))],real[l][k][i],imag[l][k][i]),(ki[tuple(sorted((i,k)))],real[l][k][j],imag[l][k][j])]:
    put(rr,var,cr);put(rr,var+78,-ci);put(ii,var,ci);put(ii,var+78,cr)
  if rr:eq.append(rr)
  if ii:eq.append(ii)
tau=mat(e1['charts']['blocks']['light_primal']['conjugation']);assert all(v.is_Rational for v in tau)
for i,j in keys:
 rr={ki[i,j]:F(-1)};ii={ki[i,j]+78:F(-1)}
 for k in range(12):
  for l in range(12):
   v=tau[k,i]*tau[l,j]
   if v:
    v=F(int(v.p),int(v.q));at=ki[tuple(sorted((k,l)))];put(rr,at,v);put(ii,at+78,-v)
 eq.extend([rr,ii])
rank=sparse_rank(eq);assert rank==153 and 156-rank==a['actual_H_invariant_metric_real_dimension']==3
G=mat(e1['charts']['blocks']['light_primal']['invariant_bilinear']);metrics={int(k):mat(p) for k,p in a['H_metric_basis'].items()};projectors={int(k):mat(p) for k,p in a['H_metric_projectors'].items()};assert set(metrics)=={1,3,8}
for n,m in metrics.items():
 pr=projectors[n];assert pr.rank()==n and pr*pr==pr and G*pr==m and m==m.T and all(v.T*m+m*v==s.zeros(12) for v in ad)
 assert s.simplify(tau.T*s.conjugate(m)*tau-m)==s.zeros(12)
for i,p in projectors.items():
 for j,q0 in projectors.items():assert p*q0==(p if i==j else s.zeros(12))
assert sum(projectors.values(),s.zeros(12))==s.eye(12)
killing=s.Matrix(12,12,lambda i,j:-s.trace(ad[i]*ad[j]));assert killing.rank()==11 and sorted([[str(k),v] for k,v in (G.inv()*killing).eigenvals().items()])==a['H_Casimir_eigenvalues']
print('STAGE independent actual_scalar_dilations_and_coupling_source_currents',flush=True)
Psi=add(*(rows(rr) for rr in e1['polynomial_parts'].values()));gf=rows(data['gauge_fixing_density']);shift={index[n]:rows(rr) for n,rr in e2['source_shifts'].items()};fullq={**rz,**{index[n]:rows(v['source_polynomial']) for n,v in e2['complete_columns'].items()}};Qpoly=operation(fullq,True);sourceS=add(*(product(elem(Jof[i]),rz[i]) for i in fields))
def gen(vector_map):return scaled(add(*(scaled(product(elem(Jof[i]),p),(-1)**par[i]) for i,p in vector_map.items() if p)),-1)
for sec,size in [('Phi',54),('Sigma',252),('phi',20),('S',2)]:
 v0={i:elem(i) for i in fields if names[i].startswith('x_'+sec+'_')};assert len(v0)==size;K0=gen(v0);V=operation(vector(K0));W=V(Psi);KK=add(K0,W);vv=vector(KK);entry=a['four_actual_scalar_dilations'][sec]
 assert K0==unpack(entry['K0']) and W==unpack(entry['W']) and KK==unpack(entry['generator'])
 assert W==scaled(add(*(product(shift[Jof[i]],p) for i,p in v0.items())),-1)
 assert {names[n]:p for n,p in vv.items() if p}=={n:unpack(p) for n,p in entry['all1286_columns'].items()}
 for i in fields:assert not add(Q(vv[i]),scaled(V(rz[i]),-1))
 assert not Qpoly(KK) and all(not vv[i] for i in fields-set(v0))
 assert all(not j and sum(n in fields for n,j in w)<=1 for p in vv.values() for gp,xp,hp,m,w in p for n,j in w)
 trace=add(*(gradient(vv[i]).get((i,()),{}) for i in fields));assert trace=={(0,0,0,0,()):F(size)} and entry['field_trace']==size
 # The SOURCE-LINEAR part's HH is zero; source-free W is retained, not set0.
 for(n,j),df in gradient(K0).items():
  if n in fields:assert not any(m in fields for m,k in gradient(df))
 assert all(not(n in sources) for gp,xp,hp,m,w in W for n,j in w)
 vg={i:elem(i) for i in fields if names[i].startswith(('B','C'))};assert len(vg)==225
Kg0=gen(vg);VG=operation(vector(Kg0));Wg=add(VG(Psi),scaled(GD(Psi),-1));Kg=add(Kg0,Wg);vv=vector(Kg);entry=a['coupling_generator'];assert Kg0==unpack(entry['K0']) and Wg==unpack(entry['W']) and Kg==unpack(entry['generator'])
assert {names[n]:p for n,p in vv.items() if p}=={n:unpack(p) for n,p in entry['all1286_columns'].items()}
for i in fields:assert not add(Q(vv[i]),scaled(VG(rz[i]),-1),GD(rz[i]))
trace=add(*(scaled(gradient(vv[i]).get((i,()),{}),(-1)**par[i]) for i in fields));assert trace=={(0,0,0,0,()):F(135)}
qkg=Qpoly(Kg);src={key:v for key,v in qkg.items() if any(n in sources for n,j in key[-1])};qgf={key:v for key,v in qkg.items() if not any(n in sources for n,j in key[-1])};thetaS=[]
for mu in range(4):thetaS.append(add(*(product(elem(Jof[index[f'B{i}_{mu}']]),elem(f'C{i}')) for i in range(45))))
assert thetaS==[unpack(p) for p in entry['source_current']] and not add(src,GD(sourceS),scaled(add(*(D(p,mu) for mu,p in enumerate(thetaS))),-1))
L=[rows(rr) for rr in e2['action_density_boundary']];ELcur=[add(GD(p),scaled(VG(p),-1)) for p in L];thetaGF=[{} for _ in range(4)]
for(i,j),df in gradient(gf).items():
 assert len(j)<=1
 if j and i in fields and vv[i]:thetaGF[j[0]]=add(thetaGF[j[0]],product(vv[i],df))
cur=[add(p,q0) for p,q0 in zip(ELcur,thetaGF)];assert cur==[unpack(p) for p in entry['complete_GF_current']] and not add(GD(gf),qgf,scaled(add(*(D(p,mu) for mu,p in enumerate(cur))),-1))
assert not add(GD(gf),scaled(VG(gf),-1),Q(Wg),scaled(add(*(D(p,mu) for mu,p in enumerate(ELcur))),-1))
reversed_control=scaled(Q(GD(Psi)),2);badn=index[entry['omitted_g_dPsi_nonboundary_control']['field']];assert summary(EL(reversed_control,{badn})[badn])==entry['omitted_g_dPsi_nonboundary_control']['Euler']
literal_omission=Q(GD(Psi));assert EL(literal_omission,{badn})[badn] and EL(reversed_control,{badn})[badn]==scaled(EL(literal_omission,{badn})[badn],2)
assert summary(add(GD(sourceS),scaled(DG(sourceS),-1)))==entry['missing_g_factor_source_control'] and add(GD(sourceS),scaled(DG(sourceS),-1))
print('STAGE independent potential_tangent_table_and_abelian_current_exclusion',flush=True)
table=[]
for term in action['local_terms']:
 if term['sector']!='PARENT_SCALAR_POTENTIAL':continue
 def fieldcount(node):
  if isinstance(node,list):return sum((fieldcount(v) for v in node),Counter())
  if isinstance(node,dict):
   if node.get('node')=='Field':return Counter({node['name'].removesuffix('Bar'):1})
   return sum((fieldcount(v) for v in node.values()),Counter())
  return Counter()
 count=fieldcount(term['term']['density'])
 for part in ['real','imag'] if term['term']['complex_monomial'] else ['real']:table.append({'coupling':term['coefficient_direction'],'component':part,'counts':{sec:count[sec] for sec in ['Phi','Sigma','phi','S']},'field_degree':sum(count.values())})
assert table==a['real34_potential_companion_count_table'] and len(table)==34
ref=get('ref')['retained_reference'];raw=ref['field_order'];Tmap=defaultdict(list)
for i,j,z in ref['physical_to_raw_kernel']['entries']:Tmap[i].append((j,rows([{'word':[],'coefficient':z}])))
px={i:add(*(product(z,elem(raw[j])) for j,z in Tmap[i])) for i in [506,507]};x=px[506];y=px[507];center=metrics[1];at=next(i for i in range(12) if any(center[i,j]!=0 for j in range(12)));ell=[center[at,j] for j in range(12)];const=lambda v:rows([{'word':[],'coefficient':str(v)}]);ac=[add(*(product(const(v),elem(f'A{j}_{mu}')) for j,v in enumerate(ell) if v)) for mu in range(4)];wc=add(*(product(const(v),elem(f'omega{j}')) for j,v in enumerate(ell) if v))
assert all(DB(p)==D(wc,mu) for mu,p in enumerate(ac))
jcur=[scaled(add(product(y,D(x,mu)),scaled(product(x,D(y,mu)),-1)),4) for mu in range(4)];mixed=add(*(scaled(product(ac[mu],jcur[mu]),(-1)**int(mu!=0)) for mu in range(4)));badn=index[a['mixed_abelian_current_Ward_failure']['omega']];assert summary(EL(DB(mixed),{badn})[badn])==a['mixed_abelian_current_Ward_failure']['Euler'] and EL(DB(mixed),{badn})[badn]
rad=add(product(x,x),product(y,y));mass=add(*(scaled(product(product(ac[mu],ac[mu]),rad),(-1)**int(mu!=0)) for mu in range(4)));badn=index[a['mixed_A2_scalar_Ward_failure']['omega']];assert summary(EL(DB(mass),{badn})[badn])==a['mixed_A2_scalar_Ward_failure']['Euler'] and EL(DB(mass),{badn})[badn]
puremass=add(*(scaled(product(ac[mu],ac[mu]),(-1)**int(mu!=0)) for mu in range(4)));long=add(*(scaled(D(ac[mu],mu),(-1)**int(mu!=0)) for mu in range(4)));assert any(EL(DB(puremass),omega).values()) and any(EL(DB(product(long,long)),omega).values())
print('STAGE independent generic_Noether_completions_and_nonnilpotent_trace_control',flush=True)
X,Y,DX,DY,BB,Gg,alpha,beta,Om,dOm=s.symbols('X Y DX DY B g a b omega domega');J=s.Matrix([[0,-1],[1,0]]);xs=s.Matrix([X,Y]);ds=s.Matrix([DX,DY]);Dx=ds+Gg*BB*J*xs;deltaDx=-Gg*Om*J*Dx;assert s.expand(Dx.dot(deltaDx))==0
lag=ds.dot(ds)/2+alpha*Gg*BB*ds.dot(J*xs)+beta*Gg**2*BB**2*xs.dot(xs)/2;dxv=-Gg*(dOm*J*xs+Om*J*ds);xv=-Gg*Om*J*xs;var=s.expand(sum(s.diff(lag,z)*v for z,v in zip([X,Y,DX,DY,BB],[*xv,*dxv,dOm])));assert s.expand(var-dOm*(Gg*(alpha-1)*ds.dot(J*xs)+Gg**2*(beta-alpha)*BB*xs.dot(xs)))==0
assert s.expand(var.subs({alpha:1,beta:1}))==0 and s.expand(var.subs({alpha:0,beta:1})) and s.expand(var.subs({alpha:1,beta:0}))
Z=s.Matrix(s.symbols('Z0:3'));K=s.Matrix(s.symbols('K0:3'));T=s.Matrix(s.symbols('T0:3'));Om3=s.Matrix(s.symbols('Om0:3'));dZ=Gg*Z.cross(Om3)-Gg*T;dK=T+Gg*K.cross(Om3);var=s.expand(Z.dot(dZ)+alpha*Gg*(dZ.dot(K)+Z.dot(dK))+beta*Gg**2*K.dot(dK));assert s.expand(var-Gg*(alpha-1)*Z.dot(T)-Gg**2*(beta-alpha)*K.dot(T))==0
assert all((i!=j and k!=l) for(i,j),(k,l) in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]])
u,v,w=s.symbols('u v w');metric=s.Matrix([[u,v],[v,w]]);assert s.solve(list(metric*J-J*metric),[v,w])=={v:0,w:u}
m2,lam=s.symbols('m2 lambda');r2=X*X+Y*Y;potential=m2*r2/2+lam*r2*r2/4;H=s.hessian(potential,[X,Y]);det=(m2+lam*r2)*(m2+3*lam*r2);assert s.expand(H.det()-det)==0;rawloop=s.cancel(s.trace(H.inv()*s.hessian(-(X*s.diff(potential,X)+Y*s.diff(potential,Y)),[X,Y]))/2);canon=s.cancel(-(X*s.diff(det,X)+Y*s.diff(det,Y))/(2*det));assert s.cancel(rawloop-canon)==-2
pt={X:1,Y:2,m2:3,lam:1};assert str(rawloop.subs(pt))==a['gaussian_nonzero_trace_control']['raw_descendant']=='-83/24' and str(canon.subs(pt))==a['gaussian_nonzero_trace_control']['canonical']=='-35/24'
programs=a['all508_physical_Euler_programs'];assert len(programs)==508 and {index[e['field']] for e in programs}==physical
for entry in programs:
 pr=e2['complete_columns'][names[Jof[index[entry['field']]]]]['physical_program'];assert pr and sha256(json.dumps(pr,sort_keys=True,separators=(',',':')).encode()).hexdigest()==entry['physical_program_sha256']
old=read(O/'primary_capture.json');assert old['execution_state']=='FAILED' and old['exit_code']==1 and 'UnboundLocalError' in old['stdout_and_stderr'] and not read(O/'failure_v1.json')['failed_counted_as_scientific_PASS']
# Proof review: the36 carrier endpoints plus rank<=4 metric pairings, independent
# full gauge/background identities and raw local-parameter equations exhaust
# this actual parity-even dimension4 module. The original four quadratic and
# full34 potential invariant counts are inherited, not freshly recomputed.
# N[A] and vacuum normalization stay separate. Unit generator loops retain W,
# raw nonzero traces, same finite conversion and reference. Constant parameter
# differentiation is not a local-g(x) QAP. Operator normalization is derived
# as delta_p*d_p O+[O,X_Hnorm], including all actual source/current terms.
assert a['physical_potential_real_directions']==34 and a['scalar_kinetic_metric_directions']==4 and a['physical_YM_metric_directions']==1 and a['pure_background_metric_directions']==3
assert not a['actual_R_coefficients_beta_functions_or_finite_values_extracted'] and not a['full_E5_A5_universal_source_adequacy_all_order_or_physical_viability_proved']
vout={'schema':'PHYSICAL_COUNTERTERM_SPAN_VALIDATION_V1','execution_state':'COMPLETED','scientific_disposition':a['scientific_disposition'],'completed_V2_native_outputs_equal':True,'raw36_carrier_and47_jet_placement_completeness_and_Noether_endpoints_reviewed':True,'actual508_physical_and48_background_difference_Ward_verified':True,'actual_H_invariant_metric_real_dimension3_by_independent_rational_realified_rank153':True,'all_three_H_metric_projectors_reality_and_invariance_verified':True,'four_scalar_dilations_all1286_columns_source_zero_and508_programs_verified':True,'weighted_coupling_all643_field_rules_source_current_and_complete_GF_current_verified':True,'potential34_companion_counts_and_polynomial_parameter_reconstruction_verified':True,'mixed_abelian_current_A2_mass_longitudinal_and_completion_controls_verified':True,'wrong_sign_and_literal_omission_g_dPsi_nonboundary_controls_verified':True,'missing_g_factor_control_and_no_inverse_physical_parameter_reviewed':True,'same_common_unit_W_insertions_nonzero_traces_and_constant_parameter_derivatives_reviewed':True,'correlated_parameter_source_background_operator_transport_and_single_counterterm_rewriting_reviewed':True,'physical_span_and_actual_formal_first_order_parameter_normalization_qualified':True,'full_E5_A5_QAP_local_coupling_arbitrary_products_or_physical_viability_qualified':False,'new_failed_native_workers':1,'new_failed_verifier_workers':0,'failed_V1_setup_source_and_capture_preserved':True,'authority_changed':False,'shared_limits':['Same actual action,representation types,old master/retract/PQR/finite trace hypotheses,software and AI author.','Independent expanded Fraction/radical checks and rational sparse elimination still share Python/SymPy parsing;not expert,experiment or Lean.','No actual R coefficient,beta function,finite normalization or physical benchmark was computed.'],'verifier_seconds_after_imports':time.perf_counter()-tick}
print('VALIDATION '+json.dumps(vout,sort_keys=True,separators=(',',':')),flush=True);watch.cancel()
