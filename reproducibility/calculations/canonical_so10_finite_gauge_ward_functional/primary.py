"""GWF1 free-word density variation, exact Euler extraction and boundary current."""
from data import *
from itertools import product,permutations
start=begin('primary');g=s.Symbol('g10');zeta=s.Symbol('zeta',real=True)
def token(kind,mu=-1,jets=()):return (kind,mu,tuple(sorted(jets)))
def field(mu):return {(token('A',mu),):s.S.One}
C={(token('c'),):s.S.One}
def plus(*ps):
 out={}
 for p in ps:
  for w,v in p.items():out[w]=s.expand(out.get(w,0)+v)
 return {w:v for w,v in out.items() if v!=0}
def scale(p,a):return {w:s.expand(a*v) for w,v in p.items() if a*v!=0}
def mul(*ps):
 out={():s.S.One}
 for p in ps:
  new={}
  for a,x in out.items():
   for b,y in p.items():new[a+b]=s.expand(new.get(a+b,0)+x*y)
  out={w:v for w,v in new.items() if v!=0}
 return out
def comm(a,b):return plus(mul(a,b),scale(mul(b,a),-1))
def partial(p,mu):
 out={}
 for w,v in p.items():
  for j,t in enumerate(w):
   u=token(t[0],t[1],t[2]+(mu,));nw=w[:j]+(u,)+w[j+1:];out[nw]=out.get(nw,0)+v
 return plus(out)
def trace(p):
 out={}
 for w,v in p.items():
  nw=min(w[j:]+w[:j] for j in range(len(w))) if w else w;out[nw]=out.get(nw,0)+v
 return plus(out)
def qA(mu):return plus(partial(C,mu),scale(comm(field(mu),C),-s.I*g))
def q(p):
 out={}
 for w,v in p.items():
  for j,t in enumerate(w):
   assert t[0]=='A';qt=qA(t[1])
   for mu in t[2]:qt=partial(qt,mu)
   out=plus(out,scale(mul({w[:j]:1},qt,{w[j+1:]:1}),v))
 return out
L2={};L3={};L4={}
for mu,nu in product(range(4),repeat=2):
 L2=plus(L2,scale(mul(partial(field(nu),mu),partial(field(nu),mu)),g*g/6))
 L3=plus(L3,scale(mul(partial(field(nu),mu),comm(field(mu),field(nu))),-2*s.I*g**3/3))
 L4=plus(L4,scale(mul(field(mu),field(mu),field(nu),field(nu)),g**4/2),scale(mul(field(mu),field(nu),field(mu),field(nu)),-5*g**4/12))
L=plus(L2,L3,L4)
# Vary every actual density factor; move the even variation to the trace front.
E=[{} for _ in range(4)];theta=[{} for _ in range(4)]
for w,v in L.items():
 for j,t in enumerate(w):
  rest={w[j+1:]+w[:j]:v};lam=t[1]
  if not t[2]:E[lam]=plus(E[lam],rest)
  else:
   assert len(t[2])==1;mu=t[2][0];E[lam]=plus(E[lam],scale(partial(rest,mu),-1));theta[mu]=plus(theta[mu],mul({(token('V',lam),):1},rest))
def substituteV(p):
 out={}
 for w,v in p.items():
  terms=[]
  for t in w:terms.append(qA(t[1]) if t[0]=='V' else {(t,):1})
  out=plus(out,scale(mul(*terms),v))
 return out
J=[trace(plus(substituteV(theta[mu]),mul(C,E[mu]))) for mu in range(4)]
W=trace(scale(plus(*(mul(C,plus(partial(E[mu],mu),scale(comm(field(mu),E[mu]),-s.I*g))) for mu in range(4))),-1))
qL=trace(q(L));divJ=trace(plus(*(partial(J[mu],mu) for mu in range(4))))
assert not trace(plus(qL,scale(W,-1),scale(divJ,-1)))
F2={}
for mu,nu in product(range(4),repeat=2):
 F=plus(partial(field(nu),mu),scale(partial(field(mu),nu),-1),scale(comm(field(mu),field(nu)),-s.I*g));F2=plus(F2,mul(F,F))
assert not trace(q(F2))
# Reconstruct all measured vertices before treating this L as a quantum input.
measured=packed(CAL/'canonical_so10_fermion_gauge_finite_difference/primary_tables.json.gz');eq=lambda a,b:s.expand(s.sympify(a)-s.sympify(b))==0
assert eq(2*s.Rational(1,6),measured['two_point_q2_delta_finite'])
p=s.symbols('p0:8');mom=[list(p[:4]),list(p[4:]),[-p[j]-p[4+j] for j in range(4)]]
vertex={}
for lor in product(range(4),repeat=3):
 ans={(0,1,2):0,(0,2,1):0}
 for word,co in L3.items():
  for perm in permutations(range(3)):
   if any(t[1]!=lor[a] for t,a in zip(word,perm)):continue
   value=co/g**3
   for t,a in zip(word,perm):
    for mu in t[2]:value*=s.I*mom[a][mu]
   nw=min(perm[j:]+perm[:j] for j in range(3));ans[nw]+=value
 key=','.join(map(str,lor));vertex[key]={''.join(map(str,w)):[str(s.expand(v).coeff(t)) for t in p] for w,v in ans.items()}
 for w,v in vertex[key].items():
  for a,b in zip(v,measured['triangle'][key][w]):assert eq(a,b)
quartic={}
for w,v in trace(L4).items():quartic[','.join(str(t[1]) for t in w)]=str(s.expand(v/g**4))
for w,v in measured['box'].items():assert eq(v,quartic.get(w,'0'))
def encp(poly):return [[[[t[0],t[1],list(t[2])] for t in w],str(v)] for w,v in sorted(poly.items())]
for poly,dim,gh in [(trace(L),4,0),(qL,5,1),(W,5,1)]+[(v,3,0) for v in E]+[(v,4,1) for v in J]:
 for w in poly:assert sum(1+len(t[2]) for t in w)==dim and sum(t[0]=='c' for t in w)==gh
no_comm=trace(scale(plus(*(mul(C,partial(E[mu],mu)) for mu in range(4))),-1))
finish('primary',{'method':'direct_free_word_density_variation_cyclic_Euler_extraction_and_boundary_current','density':encp(trace(L)),'Euler_matrices':[encp(v) for v in E],'Ward_image':encp(W),'direct_q_density':encp(qL),'boundary_current':[encp(v) for v in J],'boundary_divergence':encp(divJ),'Ward_without_covariant_commutator':encp(no_comm),'invariant_zeta_Ward_image':[],'cubic_vertex':vertex,'quartic_density':quartic,'quadratic_coefficient':'1/6','coupling':'g10','physical_spin_trace':4,'closed_family_count':3,'new_loop_integrals':0,'physical_scheme_adopted':False},start)
