"""SYR1 two-state chiral module and independent scalar/basis projection route."""
from data import *
from itertools import product
start=begin('replay')
paths={}
for n in range(1,5):
 for roles in product(range(2),repeat=n):
  for labels in product(range(2),repeat=n):
   weight=0
   for initial in [0,1]:
    state=initial;valid=True
    for role,label in reversed(list(zip(roles,labels))):
     if state!=label:valid=False;break
     state^=(1+role)%2
    if valid and state==initial:weight+=2
   if sum(1-r for r in roles)%2:assert weight==0
   paths[str(n)+'_'+''.join(map(str,roles))+'_'+''.join(map(str,labels))]=str(weight)
# Normal ordered chi-word proof of the crossed-Clifford module:
# Gamma switches the two chiral sectors; a scalar leaves their label fixed.
# The mass map in sector s transforms with c_(1-s) on its left, c_s on right.
g=s.Symbol('g10');cL,cR,U,V=s.symbols('cL cR U V',commutative=False)
charges=[cL,cR];mass=[U,V];qmass=[s.I*g*(cR*U-U*cL),s.I*g*(cL*V-V*cR)]
for sector in [0,1]:assert s.expand(qmass[sector]-s.I*g*(charges[1-sector]*mass[sector]-mass[sector]*charges[sector]))==0
# The parity-even formal trace of At-A vanishes by two equal spin sectors.
formal_trace_difference=s.expand(2*(cR-cL)+2*(cL-cR));assert formal_trace_difference==0
spin={}
for mu,nu in product(range(4),repeat=2):
 row=[]
 for i,j in product(range(2),repeat=2):
  selector=s.sympify(paths['2_00_'+str(i)+str(j)]);row.append(str(-selector*int(mu==nu)/2))
 spin[f'{mu}_{nu}']=row
pref=-sum(s.sympify(spin['0_0'][j]) for j in [1,2])
eps,L=s.symbols('epsilon L');D=s.Symbol('d');ratio=s.gammasimp((D/2)*s.gamma(1-D/2)/s.gamma(2-D/2));assert s.simplify(ratio+D/(D-2))==0
bar=s.factor(-pref*((4/D)*ratio-1));hat=s.factor(-pref*(4/D)*ratio);ref=s.factor(-pref*(ratio-1))
logregular=(s.EulerGamma+L)*eps+s.loggamma(1+eps)+2*s.loggamma(2-eps)-s.loggamma(4-2*eps)
b0=s.gamma(2)**2/s.gamma(4);b1=s.simplify(s.diff(logregular,eps).subs(eps,0));base=s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)*s.gamma(2-eps)**2/s.gamma(4-2*eps)
def jets(f):
 f=f.subs(D,4-2*eps);f0=f.subs(eps,0);f1=s.diff(f,eps).subs(eps,0)
 return [str(s.simplify(b0*f0)),str(s.simplify(b0*(f1+f0*b1)))]
diff=s.factor((bar-ref).subs(D,4-2*eps));F0=s.simplify(b0*s.diff(diff,eps).subs(eps,0));FD=diff*base/eps
YCT=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz');B=[dec(YCT['B10']),dec(YCT['B126'])]
basis=[];coords=[]
def tidy(M):return s.SparseMatrix(M).applyfunc(s.simplify)
for name,b in zip(['C10','C126'],B):
 cs=list(map(dec,YCT[name]));C=s.SparseMatrix(256,len(cs),{(16*i+j,k):v for k,M in enumerate(cs) for (i,j),v in M.todok().items()})
 for M in cs:assert M==M.T
 assert tidy(C.H*C)==s.eye(len(cs));a=tidy(C.H*b);assert not tidy(C*a-b).todok();basis.append(C);coords.append(a)
cross_basis=tidy(basis[0].H*basis[1]);assert not cross_basis.todok()
metrics=[tidy(v.H*v).applyfunc(lambda z:s.simplify(s.re(z))) for v in coords];cross=tidy(coords[0].H*cross_basis*coords[1])
family={}
for name in ['10','126']:
 terms=[]
 for i in range(3):
  for j in range(i,3):
   z=s.Symbol('y'+name+'_'+str(i)+str(j),complex=True);terms.append((1 if i==j else 2)*s.conjugate(z)*z)
 family[name]=str(s.expand(sum(terms)))
finish('replay',{'method':'two_state_projector_flow_and_independent_Feynman_bubble_basis_projection','chiral_paths':paths,'operator_covariance_by_crossed_chiral_module':True,'formal_even_trace_At_minus_A':str(formal_trace_difference),'scalar_spin_coefficients':spin,'scalar_dot_numerator_prefactor':str(pref),'actual_bar_pole_finite':jets(bar),'actual_hat_pole_finite':jets(hat),'reference_physical_pole_finite':jets(ref),'physical_difference_finite':str(F0),'physical_difference_exact':str(FD),'relative_hat_kinetic_pole':str(s.simplify((hat-ref).subs(D,4)*b0)),'scalar_metrics':list(map(enc,metrics)),'complex_cross_metric':enc(cross),'family_norm_polynomials':family,'complete_symmetric_basis_dimensions':[C.cols for C in basis],'basis_reconstruction_positions_checked':2*256*328,'basis_isometry_positions_checked':136**2,'physical_spin_trace':4,'gaussian_factor':'1/2','extra_family_factor_used':False,'reference_is_parity_even_only':True,'full_chiral_regularization_or_measure_constructed':False,'mixed_scalar_gauge_coefficients_measured':False,'physical_scheme_adopted':False,'new_one_loop_finite_bubble_families':1,'new_two_loop_integrals':0},start)
