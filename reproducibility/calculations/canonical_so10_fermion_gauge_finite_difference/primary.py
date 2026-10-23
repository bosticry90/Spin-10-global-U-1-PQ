"""GFD1 explicit split-Clifford numerator witnesses and local Laurent limits."""
from data import *
from itertools import product,permutations
start=begin('primary')
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
g4=[s.kronecker_product(pa[0],s.eye(2)),s.kronecker_product(pa[1],s.eye(2)),s.kronecker_product(pa[2],pa[0]),s.kronecker_product(pa[2],pa[1])]
gam=[s.kronecker_product(t,pa[2]) for t in g4]+[s.kronecker_product(s.eye(4),t) for t in pa[:2]]
for a,b in product(range(6),repeat=2):assert gam[a]*gam[b]+gam[b]*gam[a]==2*int(a==b)*s.eye(8)
pair={w:gam[w[0]]*gam[w[1]] for w in product(range(6),repeat=2)}
four={w:s.SparseMatrix(pair[w[:2]]*pair[w[2:]]).todok() for w in product(range(6),repeat=4)}
pair={w:s.SparseMatrix(M).todok() for w,M in pair.items()};cache={}
def tr(w):
 if w not in cache:
  A=four[w[:4]];B=pair[w[4:]] if len(w)==6 else four[w[4:]]
  cache[w]=s.expand(sum(v*B.get((j,i),0) for (i,j),v in A.items())/2)
 return cache[w]
def cyc(w):return min(w[j:]+w[:j] for j in range(len(w)))
h,eps,L=s.symbols('h epsilon L');d=4+h;m=s.Symbol('mIR2',positive=True)
radial=[]
for r,n in [(1,3),(2,4)]:
 expr=m**(-eps)*s.gamma(r+2-eps)*s.gamma(n-r-2+eps)/(s.gamma(2-eps)*s.gamma(n))
 radial.append(s.simplify(s.limit(eps*expr,eps,0)))
assert radial==[1,1]
raw3={};bar3={};fin3={}
for mu,nu,rho,j in product(range(4),repeat=4):
 samples=[]
 for rank in [0,1,2]:
  A=-sum(tr((a,mu,j,nu,a,rho)) for a in range(4+rank))
  B=-sum(tr((a,mu,a,nu,j,rho)) for a in range(4+rank))
  U=2*sum(tr((j,mu,a,nu,a,rho))+tr((a,mu,j,nu,a,rho))+tr((a,mu,a,nu,j,rho)) for a in range(4+rank))
  samples.append([A,B,U])
 for pos in range(3):assert samples[2][pos]-samples[0][pos]==2*(samples[1][pos]-samples[0][pos])
 pol=[h*(a-b) for a,b in zip(samples[1],samples[0])];raw3[mu,nu,rho,j]=pol;bar3[mu,nu,rho,j]=samples[0]
 # actual-reference=-missing; h=-2eps times a pole gives+2 d/dh.
 fin3[mu,nu,rho,j]=[s.expand(2*s.diff(z,h).subs(h,0)/den) for z,den in zip(pol,[4,4,24])]
def tri(raw,UV=False):
 out={}
 for lor in product(range(4),repeat=3):
  block={(0,1,2):[s.S.Zero]*8,(0,2,1):[s.S.Zero]*8}
  for perm in permutations(range(3)):
   a,b,c=perm;w=cyc(perm)
   for j in range(4):
    A,B,U=raw[lor[a],lor[b],lor[c],j]
    if UV:A,B,U=A/4,B/4,U/24
    for leg,val in [(a,A+B+2*U),(b,B+U)]:
     for independent in range(2):block[w][4*independent+j]+=s.Rational(1,6)*(int(leg==independent)-int(leg==2))*val
  out[','.join(map(str,lor))]={''.join(map(str,w)):list(map(str,v)) for w,v in block.items()}
 return out
bar4={};pol2={};pol4={}
for mu,nu,rho,sig in product(range(4),repeat=4):
 samples=[]
 for rank in [0,1,2]:
  vals=[s.S.Zero]*3
  for a,b in product(range(4+rank),repeat=2):
   count=int(a>=4)+int(b>=4)
   vals[count]+=tr((a,mu,a,nu,b,rho,b,sig))+tr((a,mu,b,nu,a,rho,b,sig))+tr((a,mu,b,nu,b,rho,a,sig))
  samples.append(vals)
 assert samples[0][0]==samples[1][0]==samples[2][0] and samples[2][1]==2*samples[1][1]
 bar4[mu,nu,rho,sig]=samples[0][0];pol2[mu,nu,rho,sig]=h*samples[1][1]
 pol4[mu,nu,rho,sig]=s.expand(h*samples[1][2]+h*(h-1)*(samples[2][2]-2*samples[1][2])/2)
def box(mode='finite'):
 out={cyc(w):s.S.Zero for w in product(range(4),repeat=4)}
 for w in product(range(4),repeat=4):
  if mode=='barUV':value=bar4[w]/192
  else:value=s.diff(pol2[w]+(0 if mode=='no_four_hat' else pol4[w]),h).subs(h,0)/96
  out[cyc(w)]+=value
 return {','.join(map(str,w)):str(s.expand(v)) for w,v in sorted(out.items())}
# Exact off-shell bubble; no auxiliary mass is introduced here.
bubble=s.Matrix(4,4,lambda mu,nu:s.simplify(-s.trace(gam[mu]*gam[4]*gam[nu]*gam[4])/4))
for mu,nu in product(range(4),repeat=2):assert bubble[mu,nu]==bubble[0,0]*int(mu==nu)
HH=-2*eps;beta=s.gamma(2-eps)**2/s.gamma(4-2*eps)
F=(bubble[0,0]/2)*HH*s.gamma(eps-1)*beta*s.exp((s.EulerGamma+L)*eps)
F0=s.simplify(s.limit(F,eps,0));assert s.limit(eps*F,eps,0)==0
# Reversal is a finite Clifford trace identity, independent of loop cyclicity.
words=list(cache)
for w in words:assert tr(w)==tr(w[::-1])
T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz')['Tminus']));G=s.Matrix(45,45,lambda a,b:s.simplify(s.trace(T[a]*T[b])))
finish('primary',{'method':'explicit_split_Clifford_integer_rank_witnesses_then_analytic_hat_polynomial','triangle':tri(fin3),'box':box(),'box_no_four_hat':box('no_four_hat'),'bar_reference_triangle_UV':tri(bar3,True),'bar_reference_box_UV':box('barUV'),'raw_triangle_hat_numerators':{','.join(map(str,k)):list(map(str,v)) for k,v in sorted(raw3.items())},'raw_box_two_hat_numerator':{','.join(map(str,k)):str(v) for k,v in sorted(pol2.items())},'raw_box_four_hat_numerator':{','.join(map(str,k)):str(v) for k,v in sorted(pol4.items())},'two_point_q2_delta_finite':str(F0),'bubble_hat_numerator_prefactor':str(bubble[0,0]),'two_point_difference_exact':str(F),'radial_pole_residues':list(map(str,radial)),'G':enc(G),'Clifford_reversal_words_checked':len(words),'witness_spin_trace':8,'witness_to_physical_divisor':2,'physical_spin_trace':4,'gaussian_factor':'1/2','closed_family_count':3,'analytic_hat_rank':'-2epsilon','maximum_hat_polynomial_degree':2,'reference_adopted_as_physical_scheme':False,'mass_dependent_terms_computed':False,'new_two_loop_integrals':0},start)
