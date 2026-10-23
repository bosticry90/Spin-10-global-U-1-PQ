"""BWF1 independent curvature force/matrix calculus and bilateral Ward identity."""
from data import *
from itertools import product
start=begin('replay');g=s.Symbol('g10',real=True);reg={};lookup={}
def jet(kind,mu=-1,ds=()):
 token=(kind,mu,tuple(sorted(ds)))
 if token not in lookup:
  z=s.Symbol(kind+str(mu)+'d'+''.join(map(str,token[2])),commutative=False);lookup[token]=z;reg[z]=token
 return lookup[token]
keys=[(k,mu) for k in ['L','R'] for mu in range(4)]+[('U',-1),('V',-1)]
F={key:jet(*key) for key in keys};Var={key:jet('v'+key[0],key[1]) for key in keys};U,V=F['U',-1],F['V',-1];CL,CR=jet('cL'),jet('cR')
def terms(expr):
 for term in s.Add.make_args(s.expand(expr)):
  cc,nc=term.args_cnc();co=s.Mul(*cc);word=[]
  for z in nc:
   if z.is_Pow:assert z.exp.is_Integer and z.exp>0;word.extend([z.base]*int(z.exp))
   else:word.append(z)
  if co!=0:yield co,tuple(word)
def D(expr,mu):
 out=0
 for co,w in terms(expr):
  for j,z in enumerate(w):
   kind,n,ds=reg[z];out+=co*s.Mul(*w[:j])*jet(kind,n,ds+(mu,))*s.Mul(*w[j+1:])
 return s.expand(out)
comm=lambda x,y:x*y-y*x
Q={}
for kind,C in [('L',CL),('R',CR)]:
 for mu in range(4):Q[kind,mu]=D(C,mu)-s.I*g*comm(F[kind,mu],C)
Q['U',-1]=s.I*g*(CR*U-U*CL);Q['V',-1]=s.I*g*(CL*V-V*CR)
def change(expr,q=False):
 out=0
 for co,w in terms(expr):
  for j,z in enumerate(w):
   kind,n,ds=reg[z];value=(Q if q else Var)[kind,n]
   for mu in ds:value=D(value,mu)
   out+=co*s.Mul(*w[:j])*value*s.Mul(*w[j+1:])
 return s.expand(out)
def rows(expr,cyclic=True):
 out={}
 for co,w in terms(expr):
  token=tuple(reg[z] for z in w)
  if cyclic and token:token=min(token[j:]+token[:j] for j in range(len(token)))
  out[token]=s.expand(out.get(token,0)+co)
 return [[[[k,n,list(ds)] for k,n,ds in w],str(v)] for w,v in sorted(out.items()) if v!=0]
def zero(expr):assert not rows(expr)
def rowdict(expr):return {tuple((k,n,tuple(ds)) for k,n,ds in w):s.sympify(v,locals={'g10':g}) for w,v in rows(expr)}
def fromrows(rr,rename=None):
 out=0
 for w,v in rr:out+=s.sympify(v,locals={'g10':g})*s.Mul(*(jet(rename if rename and k=='A' else k,n,ds) for k,n,ds in w))
 return out
SYR=packed(CAL/'canonical_so10_scalar_yukawa_reference/replay_tables.json.gz');MF=packed(CAL/'canonical_so10_mixed_bosonic_finite_difference/replay_tables.json.gz');GF=packed(CAL/'canonical_so10_finite_gauge_ward_functional/replay_tables.json.gz')
k=s.sympify(SYR['physical_difference_finite'])/2;a=s.I*g/3;b=2*g*g/3;c=-5*g*g/6;d=s.Rational(5,12)
Lg=0;E={key:0 for key in keys};theta=[0]*4;Ig=0
for kind in ['L','R']:
 G=[F[kind,mu] for mu in range(4)];VG=[Var[kind,mu] for mu in range(4)];S=sum(z*z for z in G)
 gd=sum(g*g*D(G[nu],mu)*D(G[nu],mu)/6-2*s.I*g**3*D(G[nu],mu)*comm(G[mu],G[nu])/3+g**4*(G[mu]**2*G[nu]**2/2-5*G[mu]*G[nu]*G[mu]*G[nu]/12) for mu,nu in product(range(4),repeat=2))/2
 Lg+=gd;zero(gd-fromrows(GF['density'],kind)/2)
 for lam in range(4):
  e2=-g*g*sum(D(D(G[lam],mu),mu) for mu in range(4))/3
  e3=-2*s.I*g**3*sum(-comm(D(G[mu],mu),G[lam])+comm(G[mu],D(G[mu],lam))-2*comm(G[mu],D(G[lam],mu)) for mu in range(4))/3
  e4=g**4*(G[lam]*S+S*G[lam]-s.Rational(5,3)*sum(G[mu]*G[lam]*G[mu] for mu in range(4)))
  E[kind,lam]=s.expand((e2+e3+e4)/2)
 for mu in range(4):theta[mu]+=(g*g*sum(VG[nu]*D(G[nu],mu) for nu in range(4))/3-2*s.I*g**3*sum(VG[nu]*comm(G[mu],G[nu]) for nu in range(4))/3)/2
 for mu,nu in product(range(4),repeat=2):
  curv=D(G[nu],mu)-D(G[mu],nu)-s.I*g*comm(G[mu],G[nu]);Ig+=curv*curv/2
L2=sum(k*D(V,mu)*D(U,mu) for mu in range(4));L3=0;L4=0
for mu in range(4):
 L,R=F['L',mu],F['R',mu];dU,dV=D(U,mu),D(V,mu)
 L3+=a*(L*(dV*U-V*dU)+R*(dU*V-U*dV));L4+=b*(L*L*V*U+R*R*U*V)+c*L*V*R*U
 E['L',mu]+=a*(dV*U-V*dU)+b*(L*V*U+V*U*L)+c*V*R*U
 E['R',mu]+=a*(dU*V-U*dV)+b*(R*U*V+U*V*R)+c*U*L*V
 E['U',-1]+=-k*D(D(V,mu),mu)+a*(2*L*dV-2*dV*R+D(L,mu)*V-V*D(R,mu))+b*(L*L*V+V*R*R)+c*L*V*R
 E['V',-1]+=-k*D(D(U,mu),mu)+a*(2*R*dU-2*dU*L+D(R,mu)*U-U*D(L,mu))+b*(U*L*L+R*R*U)+c*R*U*L
 theta[mu]+=k*(Var['V',-1]*D(U,mu)+Var['U',-1]*D(V,mu))+a*(Var['V',-1]*(U*L-R*U)+Var['U',-1]*(V*R-L*V))
Lpot=d*U*V*U*V;L4+=Lpot;E['U',-1]+=2*d*V*U*V;E['V',-1]+=2*d*U*V*U
for cand,key in [(L3,'triangle_density'),(L4-Lpot,'YYGG_density'),(Lpot,'YYYY_density')]:zero(cand-fromrows(MF[key]))
Lm=L3+L4;density=Lg+L2+Lm
zero(change(density)-sum(E[key]*Var[key] for key in keys)-sum(D(theta[mu],mu) for mu in range(4)))
J=[s.expand(theta[mu].xreplace({Var[key]:Q[key] for key in keys})+CL*E['L',mu]+CR*E['R',mu]) for mu in range(4)]
Wg=-sum(C*(D(E[kind,mu],mu)-s.I*g*comm(F[kind,mu],E[kind,mu])) for kind,C in [('L',CL),('R',CR)] for mu in range(4))
Wm=s.I*g*(CL*(V*E['V',-1]-E['U',-1]*U)+CR*(U*E['U',-1]-E['V',-1]*V));W=Wg+Wm;qL=change(density,True);divJ=sum(D(J[mu],mu) for mu in range(4));zero(qL-W-divJ)
Im=0
for mu in range(4):
 DU=D(U,mu)-s.I*g*(F['R',mu]*U-U*F['L',mu]);DV=D(V,mu)-s.I*g*(F['L',mu]*V-V*F['R',mu]);Im+=DV*DU
Iv=V*U*V*U
for inv in [Ig,Im,Iv]:zero(change(inv,True))
def bypower(expr,power):return s.expand(expr).coeff(g,power)*g**power
mis={'1':rows(L3-bypower(k*Im,1)),'2':rows(L4-Lpot-bypower(k*Im,2))}
finish('replay',{'method':'independent_curvature_force_and_matrix_calculus_with_arbitrary_variation_gate','density':rows(density),'gauge_density':rows(Lg),'scalar_kinetic_density':rows(L2),'mixed_density':rows(Lm),'Euler_matrices':{kind+str(mu):rows(E[kind,mu],False) for kind,mu in keys},'Ward_image':rows(W),'direct_q_density':rows(qL),'boundary_current':[rows(v) for v in J],'boundary_divergence':rows(divJ),'Ward_without_scalar_Euler_terms':rows(Wg),'invariant_densities':{'gauge':rows(Ig),'mass_kinetic':rows(Im),'potential':rows(Iv)},'invariant_Ward_images':{'gauge':[],'mass_kinetic':[],'potential':[]},'scalar_kinetic_covariantization_mismatches':mis,'family_trace':'FULL48_NO_EXTRA3','measured_scalar_kinetic_coefficient':str(k),'new_loop_integrals':0,'physical_scheme_adopted':False},start)
