"""GPC1 independent two-component Weyl-modulus local heat/curvature route."""
from data import *
from itertools import product
start=begin('replay')
p1=s.Matrix([[0,1],[1,0]]);p2=s.Matrix([[0,-s.I],[s.I,0]]);p3=s.diag(1,-1)
sigma=[s.eye(2),s.I*p1,s.I*p2,s.I*p3];bsigma=[s.eye(2),-s.I*p1,-s.I*p2,-s.I*p3]
for mu,nu in product(range(4),repeat=2):assert sigma[mu]*bsigma[nu]+sigma[nu]*bsigma[mu]==2*int(mu==nu)*s.eye(2)
f=s.symbols('f01 f02 f03 f12 f13 f23');pairs=[(a,b) for a in range(4) for b in range(a+1,4)];fs=dict(zip(pairs,f))
def om(mu,nu):return -s.I*(fs.get((mu,nu),0)-fs.get((nu,mu),0))
E=sum((bsigma[mu]*sigma[nu]*om(mu,nu)/2 for mu,nu in product(range(4),repeat=2)),s.zeros(2))
Eopp=sum((sigma[mu]*bsigma[nu]*om(mu,nu)/2 for mu,nu in product(range(4),repeat=2)),s.zeros(2))
O2=sum(om(mu,nu)**2 for mu,nu in product(range(4),repeat=2))*s.eye(2)
heat=s.expand((s.trace(E**2/2+O2/12)+s.trace(Eopp**2/2+O2/12))/2)
assert s.trace(E)==s.trace(Eopp)==0
# Re Gamma_W=-1/2 Tr_2 log(P): log=-integral dt exp(-tP)/t.
# A single F12 has two entries in sum_mn Fmn^2; hence divide by4.
c_heat=s.expand(heat).coeff(f[0],2)/4
assert s.expand(heat-4*c_heat*sum(z*z for z in f))==0
mom=s.symbols('p0:8');p=[list(mom[:4]),list(mom[4:]),[-mom[j]-mom[4+j] for j in range(4)]]
def canon(word):return sorted(tuple(word[j:])+tuple(word[:j]) for j in range(len(word)))[0]
def add(out,w,v):
 w=canon(w);out[w]=s.expand(out.get(w,0)+v)
triangle={}
for lor in product(range(4),repeat=3):
 ans={(0,1,2):0,(0,2,1):0}
 for mu,nu in product(range(4),repeat=2):
  F1={}
  F2={}
  for a in range(3):
   value=s.I*(p[a][mu]*int(lor[a]==nu)-p[a][nu]*int(lor[a]==mu))
   if value:F1[(a,)]=value
  for a,b in product(range(3),repeat=2):
   value=-s.I*int(lor[a]==mu)*int(lor[b]==nu)
   F2[(a,b)]=F2.get((a,b),0)+value;F2[(b,a)]=F2.get((b,a),0)-value
  for w1,v1 in F1.items():
   for w2,v2 in F2.items():
    if len(set(w1+w2))==3:
     add(ans,w1+w2,c_heat*v1*v2);add(ans,w2+w1,c_heat*v2*v1)
 triangle[','.join(map(str,lor))]={''.join(map(str,w)):[str(s.expand(z).coeff(t)) for t in mom] for w,z in ans.items()}
box={canon(w):s.S.Zero for w in product(range(4),repeat=4)}
for mu,nu in product(range(4),repeat=2):
 if mu==nu:continue
 comm={(mu,nu):-s.I,(nu,mu):s.I}
 for a,x in comm.items():
  for b,y in comm.items():add(box,a+b,c_heat*x*y)
T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz')['Tminus']));G=s.Matrix(45,45,lambda a,b:s.simplify(s.trace(T[a]*T[b])))
finish('replay',{'method':'independent_Weyl_sigma_modulus_heat_coefficient_and_curvature_expansion','triangle':triangle,'box':{','.join(map(str,k)):str(s.expand(v)) for k,v in sorted(box.items())},'Weyl_even_heat_Fpair_polynomial':str(heat),'Weyl_heat_curvature_coefficient':str(c_heat),'Weyl_spin_trace':2,'Weyl_modulus_log_factor':'1/2','full_Dirac_equivalent_log_factor':'1/4','G':enc(G),'physical_spin_trace':4,'gaussian_factor':'1/2','closed_family_count':3,'UV_only_d4_angular_projection':True,'parity_odd_computed':False,'mass_dependent_terms_computed':False,'new_one_loop_vertex_families':2,'new_two_loop_integrals':0,'physical_scheme_adopted':False},start)
