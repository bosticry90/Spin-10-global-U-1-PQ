"""GWF1 independent matrix calculus/Yang-Mills force and covariant divergence."""
from data import *
from itertools import product
start=begin('replay');g=s.Symbol('g10');reg={};lookup={}
def jet(kind,mu=-1,der=()):
 t=(kind,mu,tuple(sorted(der)))
 if t not in lookup:
  name=kind+str(mu)+'d'+''.join(map(str,t[2]));z=s.Symbol(name,commutative=False);lookup[t]=z;reg[z]=t
 return lookup[t]
A=[jet('A',mu) for mu in range(4)];V=[jet('V',mu) for mu in range(4)];C=jet('c')
def terms(expr):
 for term in s.Add.make_args(s.expand(expr)):
  cc,nc=term.args_cnc();coef=s.Mul(*cc);word=[]
  for z in nc:
   if z.is_Pow:
    assert z.exp.is_Integer and z.exp>0;word.extend([z.base]*int(z.exp))
   else:word.append(z)
  if coef!=0:yield coef,tuple(word)
def D(expr,mu):
 out=0
 for co,w in terms(expr):
  for j,z in enumerate(w):
   kind,n,der=reg[z];out+=co*s.Mul(*w[:j])*jet(kind,n,der+(mu,))*s.Mul(*w[j+1:])
 return s.expand(out)
comm=lambda x,y:x*y-y*x
qA=[D(C,mu)-s.I*g*comm(A[mu],C) for mu in range(4)]
def change(expr,mode):
 out=0
 for co,w in terms(expr):
  for j,z in enumerate(w):
   kind,mu,der=reg[z];assert kind=='A';delta=V[mu] if mode=='variation' else qA[mu]
   for dmu in der:delta=D(delta,dmu)
   out+=co*s.Mul(*w[:j])*delta*s.Mul(*w[j+1:])
 return s.expand(out)
def rows(expr,cyclic=True):
 poly={}
 for co,w in terms(expr):
  tok=tuple(reg[z] for z in w)
  if cyclic and tok:tok=min(tok[j:]+tok[:j] for j in range(len(tok)))
  poly[tok]=s.expand(poly.get(tok,0)+co)
 return [[[[t[0],t[1],list(t[2])] for t in w],str(v)] for w,v in sorted(poly.items()) if v!=0]
def zero(expr):assert not rows(expr)
L2=sum(g*g*D(A[nu],mu)*D(A[nu],mu)/6 for mu,nu in product(range(4),repeat=2))
L3=sum(-2*s.I*g**3*D(A[nu],mu)*comm(A[mu],A[nu])/3 for mu,nu in product(range(4),repeat=2))
L4=sum(g**4*(A[mu]**2*A[nu]**2/2-5*A[mu]*A[nu]*A[mu]*A[nu]/12) for mu,nu in product(range(4),repeat=2));L=L2+L3+L4
F={(mu,nu):D(A[nu],mu)-D(A[mu],nu)-s.I*g*comm(A[mu],A[nu]) for mu,nu in product(range(4),repeat=2)}
S=sum(z*z for z in A);E=[]
for lam in range(4):
 e2=-g*g*sum(D(D(A[lam],mu),mu) for mu in range(4))/3
 force=-2*g*g*sum(D(F[mu,lam],mu)-s.I*g*comm(A[mu],F[mu,lam]) for mu in range(4))/3
 e3=s.expand(force).coeff(g,3)*g**3
 e4=g**4*(A[lam]*S+S*A[lam]-s.Rational(5,3)*sum(A[nu]*A[lam]*A[nu] for nu in range(4)))
 E.append(s.expand(e2+e3+e4))
theta=[g*g*sum(V[nu]*D(A[nu],mu) for nu in range(4))/3-2*s.I*g**3*sum(V[nu]*comm(A[mu],A[nu]) for nu in range(4))/3 for mu in range(4)]
zero(change(L,'variation')-sum(E[mu]*V[mu]+D(theta[mu],mu) for mu in range(4)))
# Substitute the symmetry transformation only after the independent Euler proof.
replaceV={V[mu]:qA[mu] for mu in range(4)}
J=[s.expand(theta[mu].xreplace(replaceV)+C*E[mu]) for mu in range(4)]
W=-sum(C*(D(E[mu],mu)-s.I*g*comm(A[mu],E[mu])) for mu in range(4))
divJ=sum(D(J[mu],mu) for mu in range(4));qL=change(L,'q');zero(qL-W-divJ)
F2=sum(z*z for z in F.values());zero(change(F2,'q'))
measured=packed(CAL/'canonical_so10_fermion_gauge_finite_difference/replay_tables.json.gz');gp=packed(CAL/'canonical_so10_fermion_pure_gauge_uv/replay_tables.json.gz')
for k in measured['triangle']:
 for w in ['012','021']:
  for a,b in zip(measured['triangle'][k][w],gp['triangle'][k][w]):assert s.sympify(a)==s.sympify(b)
assert s.sympify(measured['two_point_q2_delta_finite'])/2==s.Rational(1,6)
quartic={','.join(str(t[1]) for t in w):str(s.expand(s.sympify(v)/g**4)) for ww,v in rows(L4) for w in [tuple((kind,mu,tuple(ds)) for kind,mu,ds in ww)]}
for w,v in measured['box'].items():assert s.sympify(v)==s.sympify(quartic.get(w,'0'))
no_comm=-sum(C*D(E[mu],mu) for mu in range(4))
finish('replay',{'method':'independent_matrix_variation_and_curvature_Euler_force_covariant_divergence','density':rows(L),'Euler_matrices':[rows(v,False) for v in E],'Ward_image':rows(W),'direct_q_density':rows(qL),'boundary_current':[rows(v) for v in J],'boundary_divergence':rows(divJ),'Ward_without_covariant_commutator':rows(no_comm),'invariant_zeta_Ward_image':[],'cubic_vertex':gp['triangle'],'quartic_density':quartic,'quadratic_coefficient':'1/6','coupling':'g10','physical_spin_trace':4,'closed_family_count':3,'new_loop_integrals':0,'physical_scheme_adopted':False},start)
