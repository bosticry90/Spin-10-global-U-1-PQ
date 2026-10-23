"""GFD1 Clifford pairings/metric-graph dimensions, no witness interpolation."""
from data import *
from itertools import product,permutations
from functools import lru_cache
start=begin('replay')
h,eps,L=s.symbols('h epsilon L');d=4+h
@lru_cache(None)
def pairings(indices):
 if not indices:return ((1,()),)
 first=indices[0];out=[]
 for j in range(1,len(indices)):
  rest=indices[1:j]+indices[j+1:]
  for sign,pp in pairings(rest):out.append(((-1)**(j+1)*sign,((first,indices[j]),)+pp))
 return tuple(out)
@lru_cache(None)
def contracted(word,ta='b',tb='b'):
 types={'a':ta,'b':tb};total=0;nodes=set(word)
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
   fixed={x for x in group if isinstance(x,int)};kinds={'b' if isinstance(x,int) else types[x] for x in group}
   if len(fixed)>1 or len(kinds)>1:value=0;break
   if not fixed:value*=h if 'h' in kinds else 4
  total+=value
 return s.expand(total)
raw3={};finite3={};bar3={}
# Exact Schwinger radial functions divided by their angular denominators.
# J13/d=Gamma(eps)*mIR^-eps/4; J24/[d(d+2)]=Gamma(eps)*mIR^-eps/24.
D=4-2*eps;m2=s.Symbol('mIR2',positive=True)
J13=s.gamma(3-eps)*s.gamma(eps)/(s.gamma(2-eps)*2)*m2**(-eps)
J24=s.gamma(4-eps)*s.gamma(eps)/(s.gamma(2-eps)*6)*m2**(-eps)
assert s.gammasimp(J13/D-s.gamma(eps)*m2**(-eps)/4)==0
assert s.gammasimp(J24/(D*(D+2))-s.gamma(eps)*m2**(-eps)/24)==0
assert s.limit(eps*s.gamma(eps),eps,0)==1
def finite(poly,den):return s.simplify(s.limit(-poly.subs(h,-2*eps)/eps,eps,0)/den)
for mu,nu,rho,j in product(range(4),repeat=4):
 A=-contracted(('a',mu,j,nu,'a',rho),'h');B=-contracted(('a',mu,'a',nu,j,rho),'h')
 U=2*(contracted((j,mu,'a',nu,'a',rho),'h')+contracted(('a',mu,j,nu,'a',rho),'h')+contracted(('a',mu,'a',nu,j,rho),'h'))
 raw3[mu,nu,rho,j]=[A,B,U];finite3[mu,nu,rho,j]=[finite(z,den) for z,den in zip([A,B,U],[4,4,24])]
def canon(w):return sorted(tuple(w[j:])+tuple(w[:j]) for j in range(len(w)))[0]
triangle={}
for lor in product(range(4),repeat=3):
 out={(0,1,2):[s.S.Zero]*8,(0,2,1):[s.S.Zero]*8}
 for perm in permutations(range(3)):
  a,b,c=perm;w=canon(perm)
  for j in range(4):
   A,B,U=finite3[lor[a],lor[b],lor[c],j]
   coeff=[A+B+2*U,B+U,0]
   for leg,val in zip([a,b,c],coeff):
    for n in range(2):out[w][4*n+j]+=val*s.Rational(1,6)*(int(leg==n)-int(leg==2))
 triangle[','.join(map(str,lor))]={''.join(map(str,w)):list(map(str,v)) for w,v in out.items()}
pol2={};pol4={};box={canon(w):s.S.Zero for w in product(range(4),repeat=4)}
for mu,nu,rho,sig in product(range(4),repeat=4):
 words=[('a',mu,'a',nu,'b',rho,'b',sig),('a',mu,'b',nu,'a',rho,'b',sig),('a',mu,'b',nu,'b',rho,'a',sig)]
 two=sum(contracted(w,'h','b')+contracted(w,'b','h') for w in words);four=sum(contracted(w,'h','h') for w in words)
 pol2[mu,nu,rho,sig]=s.expand(two);pol4[mu,nu,rho,sig]=s.expand(four)
 box[canon((mu,nu,rho,sig))]+=finite(two+four,24)/8
trace_hat=contracted((0,'a',0,'a'),'h');prefactor=s.expand(-trace_hat/2)
# The independent shifted bubble uses J2/I2=-d*Delta/(d-2).
reg=s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)*s.gamma(2-eps)**2/s.gamma(4-2*eps)
F=s.factor((-prefactor/(d-2)).subs(h,-2*eps))*reg/eps
F0=s.simplify(s.limit(F,eps,0))
T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz')['Tminus']));G=s.Matrix(45,45,lambda a,b:s.simplify(s.trace(T[a]*T[b])))
finish('replay',{'method':'independent_Clifford_pairing_metric_graphs_with_formal_hat_dimension','triangle':triangle,'box':{','.join(map(str,w)):str(s.expand(v)) for w,v in sorted(box.items())},'raw_triangle_hat_numerators':{','.join(map(str,k)):list(map(str,v)) for k,v in sorted(raw3.items())},'raw_box_two_hat_numerator':{','.join(map(str,k)):str(v) for k,v in sorted(pol2.items())},'raw_box_four_hat_numerator':{','.join(map(str,k)):str(v) for k,v in sorted(pol4.items())},'two_point_q2_delta_finite':str(F0),'two_point_difference_exact':str(F),'bubble_hat_numerator_prefactor':str(s.expand(prefactor/h)),'G':enc(G),'pairing_counts_six_eight':[len(pairings(tuple(range(n)))) for n in [6,8]],'physical_spin_trace':4,'gaussian_factor':'1/2','closed_family_count':3,'analytic_hat_rank':'-2epsilon','maximum_hat_polynomial_degree':2,'reference_adopted_as_physical_scheme':False,'mass_dependent_terms_computed':False,'new_two_loop_integrals':0},start)
