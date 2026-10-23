"""MBF1 independent metric graphs, path algebra and actual Schur control."""
from data import *
from itertools import product,combinations
from functools import lru_cache
start=begin('replay');g=s.Symbol('g10',real=True);h,eps=s.symbols('h epsilon')
@lru_cache(None)
def pairings(indices):
 if not indices:return ((1,()),)
 out=[]
 for j in range(1,len(indices)):
  for sign,pp in pairings(indices[1:j]+indices[j+1:]):out.append(((-1)**(j+1)*sign,((indices[0],indices[j]),)+pp))
 return tuple(out)
@lru_cache(None)
def graph(word,ta='b',tb='b'):
 domains={'a':ta,'b':tb};nodes=set(word);result=0
 for sign,pp in pairings(tuple(range(len(word)))):
  parent={x:x for x in nodes}
  def root(x):
   while parent[x]!=x:x=parent[x]
   return x
  for i,j in pp:
   a,b=root(word[i]),root(word[j])
   if a!=b:parent[a]=b
  groups={}
  for x in nodes:groups.setdefault(root(x),set()).add(x)
  value=4*sign
  for group in groups.values():
   fixed={x for x in group if isinstance(x,int)};types={'b' if isinstance(x,int) else domains[x] for x in group}
   if len(fixed)>1 or len(types)>1:value=0;break
   if not fixed:value*=h if 'h' in types else 4
  result+=value
 return s.expand(result)
def word(indices,v):
 out=[]
 for k,mu in zip(indices,v):
  out.append(k)
  if mu>=0:out.append(mu)
 return tuple(out)
def finite(poly,den):return s.simplify(s.limit(-poly.subs(h,-2*eps)/eps,eps,0)/den)
assert s.limit(eps*s.gamma(eps),eps,0)==1
D=4-2*eps;m2=s.Symbol('mIR2',positive=True)
for r,n,den in [(1,3,D),(2,4,D*(D+2))]:
 exact=s.gamma(r+D/2)*s.gamma(n-r-D/2)/(s.gamma(D/2)*s.gamma(n))*m2**(-eps)
 assert s.gammasimp(exact/den-s.gamma(eps)*m2**(-eps)/(4 if r==1 else 24))==0
raw3={};f3={}
for pos in range(3):
 for mu,j in product(range(4),repeat=2):
  v=tuple(mu if k==pos else -1 for k in range(3))
  A=-graph(word(('a',j,'a'),v),'h');B=-graph(word(('a','a',j),v),'h')
  U=2*(graph(word((j,'a','a'),v),'h')+graph(word(('a',j,'a'),v),'h')+graph(word(('a','a',j),v),'h'))
  raw3[v,j]=[A,B,U];f3[v,j]=[finite(z,den) for z,den in zip([A,B,U],[4,4,24])]
def selectors(v):
 n=len(v);ng=sum(mu>=0 for mu in v);phase=s.simplify(s.Rational((-1)**n,2*n)*(-s.I)**n*(-s.I*g)**ng)
 for labs in product(range(2),repeat=n):
  count=0
  for initial in [0,1]:
   state=initial;ok=True
   for mu,lab in reversed(list(zip(v,labs))):
    if state!=lab:ok=False;break
    state^=(1+int(mu>=0))%2
   if ok and state==initial:count+=1
  if count:yield labs,s.Rational(count,2),phase

def canon(w):return sorted(tuple(w[j:])+tuple(w[:j]) for j in range(len(w)))[0]
def add(out,w,v):
 key=canon(w);out[key]=s.expand(out.get(key,0)+v)
def fields(v,labs):return tuple(('L' if lab==0 else 'R',mu,()) if mu>=0 else ('U' if lab==0 else 'V',-1,()) for mu,lab in zip(v,labs))
def rows(p):return [[[[kind,mu,list(ds)] for kind,mu,ds in w],str(v)] for w,v in sorted(p.items()) if v!=0]
tri={}
for (v,j),vals in f3.items():
 A,B,U=vals
 for labs,pweight,phase in selectors(v):
  tokens=fields(v,labs)
  for pos,kernel in [(0,A+B+2*U),(1,B+U)]:
   ww=list(tokens);kind,mu,ds=ww[pos];ww[pos]=(kind,mu,(j,));add(tri,tuple(ww),phase*pweight*(-s.I)*kernel)
vs=set()
for a,b in combinations(range(4),2):
 for mu,nu in product(range(4),repeat=2):vs.add(tuple(mu if k==a else nu if k==b else -1 for k in range(4)))
vs.add((-1,)*4);p2={};p4={};boxes={'YYGG':{},'YYYY':{}}
for v in sorted(vs):
 patterns=[('a','a','b','b'),('a','b','a','b'),('a','b','b','a')]
 two=sum(graph(word(kk,v),'h','b')+graph(word(kk,v),'b','h') for kk in patterns);four=sum(graph(word(kk,v),'h','h') for kk in patterns)
 p2[v]=s.expand(two);p4[v]=s.expand(four);f=finite(two+four,24)
 for labs,pweight,phase in selectors(v):add(boxes['YYYY' if all(mu<0 for mu in v) else 'YYGG'],fields(v,labs),phase*pweight*f)
# Third route to the scalar4 coefficient: actual P/S Schur determinant.
x,y,m,z=s.symbols('barp2 hatp2 m z',positive=True);B=s.sqrt(x)*s.diag(1,1,-1,-1);H=s.sqrt(y)*s.BlockMatrix([[s.zeros(2),s.eye(2)],[s.eye(2),s.zeros(2)]]).as_explicit()
S=s.I*B;P=m*s.eye(4)+s.I*B;mix=s.I*H;schur=s.simplify(P-mix*S.inv()*mix);schur0=s.simplify(schur.subs(m,0));ratio=s.factor(schur.det()/schur0.det())
assert s.factor(ratio-(1+m*m*x/(x+y)**2)**2)==0
log_second=s.expand(s.series(-s.log(1+z),z,0,3).removeO()).coeff(z,2)
bar_rank=4;angular=bar_rank*(bar_rank+2)/(D*(D+2));schur_finite=s.simplify(s.limit(log_second*(angular-1)/eps,eps,0))
finish('replay',{'method':'formal_metric_pairing_graphs_and_independent_chiral_path_phase_derivation','triangle_density':rows(tri),'YYGG_density':rows(boxes['YYGG']),'YYYY_density':rows(boxes['YYYY']),'raw_triangle_hat_numerators':{','.join(map(str,v))+':'+str(j):list(map(str,q)) for (v,j),q in sorted(raw3.items())},'raw_box_two_hat_numerator':{','.join(map(str,v)):str(q) for v,q in sorted(p2.items())},'raw_box_four_hat_numerator':{','.join(map(str,v)):str(q) for v,q in sorted(p4.items())},'Schur_normalized_det_ratio':str(ratio),'Schur_scalar4_coefficient':str(schur_finite),'Schur_constant_mass_is_control_only':True,'physical_spin_trace':4,'gaussian_factor':'1/2','path_trace_factor':'1/2_FOR_EACH_ALLOWED_PATH','family_trace':'FULL48_NO_EXTRA3','hat_rank':'-2epsilon','raw_triangle_positions':144,'raw_box_positions':194,'new_one_loop_finite_families':3,'new_two_loop_integrals':0,'physical_scheme_adopted':False,'finite_massive_threshold_computed':False},start)
