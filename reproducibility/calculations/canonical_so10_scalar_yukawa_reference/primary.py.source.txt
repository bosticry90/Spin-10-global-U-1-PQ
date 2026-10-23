"""SYR1 explicit chiral reference algebra, actual Nambu scalar trace and bubble."""
from data import *
from itertools import product
start=begin('primary')
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
g4=[s.kronecker_product(pa[0],s.eye(2)),s.kronecker_product(pa[1],s.eye(2)),s.kronecker_product(pa[2],pa[0]),s.kronecker_product(pa[2],pa[1])]
gam=[s.kronecker_product(t,pa[2]) for t in g4]+[s.kronecker_product(s.eye(4),t) for t in pa[:2]]
chi_actual=s.prod(gam[:4]);chi_ref=s.I*s.prod(gam)
def tidy(M):return s.SparseMatrix(M).applyfunc(s.expand)
def zero(M):assert not tidy(M).todok()
for a,b in product(range(6),repeat=2):zero(gam[a]*gam[b]+gam[b]*gam[a]-2*int(a==b)*s.eye(8))
zero(chi_actual**2-s.eye(8));zero(chi_ref**2-s.eye(8))
for j in range(6):zero(gam[j]*chi_ref+chi_ref*gam[j]);zero(gam[j]*chi_actual+chi_actual*gam[j] if j<4 else gam[j]*chi_actual-chi_actual*gam[j])
paths={}
for n in range(1,5):
 for roles in product(range(2),repeat=n):
  for labels in product(range(2),repeat=n):
   values=[]
   for chi in [chi_actual,chi_ref]:
    traces=0
    for orientation in [1,-1]:
     Ps=[(s.eye(8)+orientation*chi)/2,(s.eye(8)-orientation*chi)/2];mat=s.eye(8)
     for role,label in zip(roles,labels):mat=mat*gam[0]*(gam[0]*Ps[label] if role else Ps[label])
     traces+=s.trace(mat)
    values.append(s.expand(traces/4)) # witness8/2 and even orientation average1/2.
   assert values[0]==values[1]
   paths[str(n)+'_'+''.join(map(str,roles))+'_'+''.join(map(str,labels))]=str(values[0])
# Exact generic operator covariance, not a fitted loop relation.
g=s.Symbol('g10');cL,cR,bL,bR,dcL,dcR,U,V=s.symbols('cL cR bL bR dcL dcR U V',commutative=False)
PL=(s.eye(8)+chi_ref)/2;PR=s.eye(8)-PL;A=PL*cL+PR*cR;At=PR*cL+PL*cR;B=PL*bL+PR*bR;dc=PL*dcL+PR*dcR;Mass=PL*U+PR*V
for mat in gam:zero(mat*A-At*mat)
qMass=PL*s.I*g*(cR*U-U*cL)+PR*s.I*g*(cL*V-V*cR);zero(qMass-s.I*g*(At*Mass-Mass*A))
qB=dc-s.I*g*(B*A-A*B)
for mat in gam[:4]:zero(-s.I*g*mat*qB-(-s.I*g*mat*dc+g*g*(At*mat*B-mat*B*A)))
PLa=(s.eye(8)+chi_actual)/2;PRa=s.eye(8)-PLa;Aa=PLa*cL+PRa*cR;Ata=PRa*cL+PLa*cR
wrong_hat=sum(len(tidy(mat*Aa-Ata*mat).todok()) for mat in gam[4:]);assert wrong_hat>0
wrong_mass=tidy(PL*s.I*g*(cL*U-U*cL)+PR*s.I*g*(cR*V-V*cR)-qMass);assert wrong_mass.todok()
# Actual source qS0 and mass law are frozen physical inputs, not replaced.
action=(CAL/'canonical_so10_sterile_matter_action/ACTION_V1.md').read_text(encoding='utf-8');assert 'qS=0' in action and 'qM = -ig' in action
spin={}
for mu,nu in product(range(4),repeat=2):
 table=[]
 for i,j in product(range(2),repeat=2):
  val=0
  for sign in [1,-1]:
   P=[(s.eye(8)+sign*chi_actual)/2,(s.eye(8)-sign*chi_actual)/2];val+=s.trace(gam[mu]*P[i]*gam[nu]*P[j])
  table.append(str(s.expand(-val/8))) # physical trace4, parity average, Nambu second derivative half.
 spin[f'{mu}_{nu}']=table
pref=-sum(s.sympify(spin['0_0'][j]) for j in [1,2])
eps,L=s.symbols('epsilon L');d=4-2*eps;h=-2*eps;beta=s.gamma(2-eps)**2/s.gamma(4-2*eps);master=s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)*beta
bar_factor=pref*(4/(d-2)+1);hat_factor=pref*4/(d-2);ref_factor=pref*(d/(d-2)+1)
def jets(f):
 regular=f*master
 return [str(s.simplify(regular.subs(eps,0))),str(s.simplify(s.diff(regular,eps).subs(eps,0)))]
Cbar=bar_factor*master/eps;Chat=hat_factor*master/eps;Cref=ref_factor*master/eps
FD=(pref*h/2)*s.gamma(eps-1)*beta*s.exp((s.EulerGamma+L)*eps)
assert s.simplify(s.gammasimp(Cbar-Cref-FD))==0
F0=s.simplify(s.limit(FD,eps,0));odd=s.simplify(s.trace(chi_actual*s.prod(gam[:4]))/2);assert odd!=0
YCT=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');Bs=[dec(YCT['B10']),dec(YCT['B126'])];metrics=[tidy(B.H*B).applyfunc(lambda z:s.simplify(s.re(z))) for B in Bs];cross=tidy(Bs[0].H*Bs[1]).applyfunc(s.simplify)
family={}
for name in ['10','126']:
 ys=s.symbols(' '.join('y'+name+'_'+str(i)+str(j) for i in range(3) for j in range(i,3)),complex=True);k=0;Y=s.zeros(3)
 for i in range(3):
  for j in range(i,3):Y[i,j]=Y[j,i]=ys[k];k+=1
 family[name]=str(s.expand(s.trace(Y.H*Y)))
finish('primary',{'method':'explicit_split_spinor_chiral_covariance_and_direct_Nambu_bubble','chiral_paths':paths,'operator_kinetic_covariance_positions':6*64,'operator_gauge_covariance_positions':4*64,'operator_mass_covariance_positions':64,'physical_BMHV_wrong_full_hat_covariance_nonzero_positions':wrong_hat,'wrong_adjoint_mass_law_nonzero_positions':len(wrong_mass.todok()),'scalar_spin_coefficients':spin,'scalar_dot_numerator_prefactor':str(pref),'actual_bar_pole_finite':jets(bar_factor),'actual_hat_pole_finite':jets(hat_factor),'reference_physical_pole_finite':jets(ref_factor),'physical_difference_finite':str(F0),'physical_difference_exact':str(FD),'relative_hat_kinetic_pole':str(s.simplify((hat_factor-ref_factor).subs(eps,0)*master.subs(eps,0))),'scalar_metrics':list(map(enc,metrics)),'complex_cross_metric':enc(cross),'family_norm_polynomials':family,'physical_odd_chi_four_gamma_trace_discarded':str(odd),'physical_spin_trace':4,'witness_spin_trace':8,'witness_to_physical_divisor':2,'gaussian_factor':'1/2','extra_family_factor_used':False,'reference_is_parity_even_only':True,'full_chiral_regularization_or_measure_constructed':False,'mixed_scalar_gauge_coefficients_measured':False,'physical_scheme_adopted':False,'new_one_loop_finite_bubble_families':1,'new_two_loop_integrals':0},start)
