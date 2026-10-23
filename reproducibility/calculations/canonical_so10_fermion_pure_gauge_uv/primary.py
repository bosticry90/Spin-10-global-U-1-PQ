"""GPC1 actual ordered Nambu triangle Taylor and box angular residues."""
from data import *
from itertools import product,permutations
from functools import lru_cache
start=begin('primary')
action=(CAL/'canonical_so10_sterile_matter_action/ACTION_V1.md').read_text(encoding='utf-8');assert 'Every gauge and Yukawa vertex acts on P.' in action
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
gamma=[s.kronecker_product(pa[1],mat) for mat in pa]+[s.kronecker_product(pa[0],s.eye(2))];PL=s.diag(1,1,0,0);PR=s.eye(4)-PL
pair={w:gamma[w[0]]*gamma[w[1]] for w in product(range(4),repeat=2)}
four={w:pair[w[:2]]*pair[w[2:]] for w in product(range(4),repeat=4)}
def trprod(A,B):return s.expand(sum(v*B[j,i] for (i,j),v in s.SparseMatrix(A).todok().items()))
@lru_cache(None)
def trace_even(w):
 A=four[w[:4]];B=pair[w[4:]] if len(w)==6 else four[w[4:]]
 left=trprod(PL*A,B);right=trprod(PR*A,B)
 assert left+right==trprod(A,B)
 return s.expand((left+right)/2)
# Each Nambu chiral trace is parity-even projected. Right color order is
# reversed by transpose, with(-1)^n from its actual charge.
def cyclic(w):return min(w[k:]+w[:k] for k in range(len(w)))
def dumpdict(d):return {','.join(map(str,k)):str(s.expand(v)) for k,v in sorted(d.items())}
eps=s.Symbol('epsilon');d=4-2*eps;m2=s.Symbol('mIR2',positive=True)
radial=[]
for power,den in [(1,3),(2,4)]:
 expr=m2**(-eps)*s.gamma(power+d/2)*s.gamma(den-power-d/2)/(s.gamma(d/2)*s.gamma(den))
 radial.append(s.simplify(s.limit(eps*expr,eps,0)))
assert radial==[1,1]
raw3={}
for mu,nu,rho,j in product(range(4),repeat=4):
 A=-sum(trace_even((a,mu,j,nu,a,rho)) for a in range(4))/4
 B=-sum(trace_even((a,mu,a,nu,j,rho)) for a in range(4))/4
 U=sum(trace_even((j,mu,a,nu,a,rho))+trace_even((a,mu,j,nu,a,rho))+trace_even((a,mu,a,nu,j,rho)) for a in range(4))/12
 raw3[mu,nu,rho,j]=[s.expand(A),s.expand(B),s.expand(U)]
def triangle(mode='actual'):
 out={}
 for lor in product(range(4),repeat=3):
  block={w:[s.S.Zero]*8 for w in [(0,1,2),(0,2,1)]}
  for perm in permutations(range(3)):
   a,b,c=perm;w=cyclic(perm);rw=cyclic(perm[::-1] if mode!='no_right_reversal' else perm)
   for j in range(4):
    A,B,U=raw3[lor[a],lor[b],lor[c],j]
    if mode=='no_denominator':U=0
    for leg,val in [(a,A+B+2*U),(b,B+U)]:
     if mode=='wrong_routing':val=-val
     for independent in range(2):
      factor=int(leg==independent)-int(leg==2)
      block[w][4*independent+j]+=s.Rational(1,6)*factor*val
      block[rw][4*independent+j]+=s.Rational(1,6)*factor*val*(1 if mode=='wrong_right_sign' else -1)
  out[','.join(map(str,lor))]={''.join(map(str,w)):list(map(str,vals)) for w,vals in block.items()}
 return out
raw4={}
for mu,nu,rho,sig in product(range(4),repeat=4):
 vals=[s.S.Zero]*3
 for a,b in product(range(4),repeat=2):
  vals[0]+=trace_even((a,mu,a,nu,b,rho,b,sig))
  vals[1]+=trace_even((a,mu,b,nu,a,rho,b,sig))
  vals[2]+=trace_even((a,mu,b,nu,b,rho,a,sig))
 raw4[mu,nu,rho,sig]=[v/24 for v in vals]
def box(missing=False):
 out={cyclic(w):s.S.Zero for w in product(range(4),repeat=4)}
 for word,vals in raw4.items():
  v=sum(vals[:2] if missing else vals)/8
  out[cyclic(word)]+=v;out[cyclic(word[::-1])]+=v
 return dumpdict(out)
T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz')['Tminus']))
G=s.Matrix(45,45,lambda a,b:s.simplify(s.trace(T[a]*T[b])))
for t in T:assert t==t.conjugate().T and s.trace(t)==0
# Universal transpose identity is separately represented in the color-word map.
finish('primary',{'method':'actual_Nambu_determinant_triangle_Taylor_box_explicit_spin_trace','triangle':triangle(),'box':box(),'raw_triangle_A_B_U':{','.join(map(str,k)):list(map(str,v)) for k,v in sorted(raw3.items())},'raw_box_three_pairings':{','.join(map(str,k)):list(map(str,v)) for k,v in sorted(raw4.items())},'triangle_no_denominator':triangle('no_denominator'),'triangle_no_right_reversal':triangle('no_right_reversal'),'triangle_wrong_right_sign':triangle('wrong_right_sign'),'triangle_wrong_routing':triangle('wrong_routing'),'box_missing_pairing':box(True),'G':enc(G),'radial_pole_residues':list(map(str,radial)),'explicit_trace_words_evaluated':trace_even.cache_info().currsize,'physical_spin_trace':4,'gaussian_factor':'1/2','closed_family_count':3,'UV_only_d4_angular_projection':True,'parity_odd_computed':False,'mass_dependent_terms_computed':False,'new_one_loop_vertex_families':2,'new_two_loop_integrals':0,'physical_scheme_adopted':False},start)
