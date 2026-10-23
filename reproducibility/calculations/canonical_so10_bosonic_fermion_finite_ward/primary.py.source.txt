"""BWF1 measured-word assembly and direct Euler/boundary extraction."""
from data import *
from itertools import product
start=begin('primary');g=s.Symbol('g10',real=True)
def tok(k,mu=-1,ds=()):return (k,mu,tuple(sorted(ds)))
def field(k,mu=-1):return {(tok(k,mu),):s.S.One}
keys=[(k,mu) for k in ['L','R'] for mu in range(4)]+[('U',-1),('V',-1)]
CL,CR=field('cL'),field('cR')
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
comm=lambda a,b:plus(mul(a,b),scale(mul(b,a),-1))
def partial(p,mu):
 out={}
 for w,v in p.items():
  for j,t in enumerate(w):
   nw=w[:j]+(tok(t[0],t[1],t[2]+(mu,)),)+w[j+1:];out[nw]=out.get(nw,0)+v
 return plus(out)
def trace(p):
 out={}
 for w,v in p.items():
  nw=min(w[j:]+w[:j] for j in range(len(w))) if w else w;out[nw]=out.get(nw,0)+v
 return plus(out)
def decode(rows,rename=None):
 out={}
 for ww,v in rows:
  w=tuple(tok(rename if rename and k=='A' else k,mu,ds) for k,mu,ds in ww);out[w]=s.sympify(v,locals={'g10':g})
 return out
GF=packed(CAL/'canonical_so10_finite_gauge_ward_functional/primary_tables.json.gz');MF=packed(CAL/'canonical_so10_mixed_bosonic_finite_difference/primary_tables.json.gz');SYR=packed(CAL/'canonical_so10_scalar_yukawa_reference/primary_tables.json.gz')
Lg=scale(plus(decode(GF['density'],'L'),decode(GF['density'],'R')),s.Rational(1,2));Lm=plus(*(decode(MF[k]) for k in ['triangle_density','YYGG_density','YYYY_density']))
k=s.sympify(SYR['physical_difference_finite'])/2;U,V=field('U'),field('V');L2=plus(*(scale(mul(partial(V,mu),partial(U,mu)),k) for mu in range(4)));L=plus(Lg,L2,Lm)
def qfield(kind,mu=-1):
 if kind in ['L','R']:
  C=CL if kind=='L' else CR
  return plus(partial(C,mu),scale(comm(field(kind,mu),C),-s.I*g))
 if kind=='U':return scale(plus(mul(CR,U),scale(mul(U,CL),-1)),s.I*g)
 assert kind=='V';return scale(plus(mul(CL,V),scale(mul(V,CR),-1)),s.I*g)
def q(poly):
 out={}
 for w,v in poly.items():
  for j,t in enumerate(w):
   qt=qfield(t[0],t[1])
   for mu in t[2]:qt=partial(qt,mu)
   out=plus(out,scale(mul({w[:j]:1},qt,{w[j+1:]:1}),v))
 return out
E={key:{} for key in keys};theta=[{} for _ in range(4)]
for w,v in L.items():
 for j,t in enumerate(w):
  rest={w[j+1:]+w[:j]:v};key=t[:2]
  if not t[2]:E[key]=plus(E[key],rest)
  else:
   assert len(t[2])==1;mu=t[2][0];E[key]=plus(E[key],scale(partial(rest,mu),-1));theta[mu]=plus(theta[mu],mul({(tok('v'+t[0],t[1]),):1},rest))
def qtheta(poly):
 out={}
 for w,v in poly.items():
  factors=[qfield(t[0][1:],t[1]) if t[0].startswith('v') else {(t,):1} for t in w];out=plus(out,scale(mul(*factors),v))
 return out
J=[trace(plus(qtheta(theta[mu]),mul(CL,E['L',mu]),mul(CR,E['R',mu]))) for mu in range(4)]
Wg=scale(plus(*(mul(C,plus(partial(E[kind,mu],mu),scale(comm(field(kind,mu),E[kind,mu]),-s.I*g))) for kind,C in [('L',CL),('R',CR)] for mu in range(4))),-1)
Wmass=scale(plus(mul(CL,plus(mul(V,E['V',-1]),scale(mul(E['U',-1],U),-1))),mul(CR,plus(mul(U,E['U',-1]),scale(mul(E['V',-1],V),-1)))),s.I*g)
W=trace(plus(Wg,Wmass));qL=trace(q(L));divJ=trace(plus(*(partial(J[mu],mu) for mu in range(4))));assert not trace(plus(qL,scale(W,-1),scale(divJ,-1)))
Ig={};Im={}
for mu,nu in product(range(4),repeat=2):
 for kind in ['L','R']:
  F=plus(partial(field(kind,nu),mu),scale(partial(field(kind,mu),nu),-1),scale(comm(field(kind,mu),field(kind,nu)),-s.I*g));Ig=plus(Ig,scale(mul(F,F),s.Rational(1,2)))
for mu in range(4):
 DU=plus(partial(U,mu),scale(plus(mul(field('R',mu),U),scale(mul(U,field('L',mu)),-1)),-s.I*g))
 DV=plus(partial(V,mu),scale(plus(mul(field('L',mu),V),scale(mul(V,field('R',mu)),-1)),-s.I*g));Im=plus(Im,mul(DV,DU))
Iv=mul(V,U,V,U)
for invariant in [Ig,Im,Iv]:assert not trace(q(invariant))
def component(p,power):return plus({w:s.expand(v).coeff(g,power)*g**power for w,v in p.items()})
missing_cov={}
for power,source in [(1,decode(MF['triangle_density'])),(2,decode(MF['YYGG_density']))]:missing_cov[str(power)]=trace(plus(source,scale(component(scale(Im,k),power),-1)))
def encp(poly):return [[[[t[0],t[1],list(t[2])] for t in w],str(v)] for w,v in sorted(poly.items())]
for poly,dim,gh in [(trace(L),4,0),(qL,5,1),(W,5,1)]+[(v,3,0) for v in E.values()]+[(v,4,1) for v in J]:
 for w in poly:assert sum(1+len(t[2]) for t in w)==dim and sum(t[0] in ['cL','cR'] for t in w)==gh
finish('primary',{'method':'assembled_measured_words_direct_cyclic_Euler_extraction_and_bilateral_Ward','density':encp(trace(L)),'gauge_density':encp(trace(Lg)),'scalar_kinetic_density':encp(trace(L2)),'mixed_density':encp(trace(Lm)),'Euler_matrices':{kind+str(mu):encp(E[kind,mu]) for kind,mu in keys},'Ward_image':encp(W),'direct_q_density':encp(qL),'boundary_current':[encp(v) for v in J],'boundary_divergence':encp(divJ),'Ward_without_scalar_Euler_terms':encp(trace(Wg)),'invariant_densities':{'gauge':encp(trace(Ig)),'mass_kinetic':encp(trace(Im)),'potential':encp(trace(Iv))},'invariant_Ward_images':{'gauge':[],'mass_kinetic':[],'potential':[]},'scalar_kinetic_covariantization_mismatches':{key:encp(v) for key,v in missing_cov.items()},'family_trace':'FULL48_NO_EXTRA3','measured_scalar_kinetic_coefficient':str(k),'new_loop_integrals':0,'physical_scheme_adopted':False},start)
