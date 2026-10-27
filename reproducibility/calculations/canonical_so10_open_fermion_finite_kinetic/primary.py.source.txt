"""OFK1 explicit projected Clifford chains and complete shifted bubbles."""
from data import *
from itertools import product
start=begin('primary')
def z(M):assert not s.SparseMatrix(M).applyfunc(s.expand).todok()
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
g4=[s.kronecker_product(pa[1],a) for a in pa]+[s.kronecker_product(pa[0],s.eye(2))]
gs=[s.kronecker_product(g,pa[2]) for g in g4]+[s.kronecker_product(s.eye(4),a) for a in pa[:2]]
chi4=s.prod(g4);chib=s.prod(gs[:4]);chia=s.I*s.prod(gs);Z=chia*chib;Pe=(s.eye(8)+Z)/2
for a,b in product(range(6),repeat=2):z(gs[a]*gs[b]+gs[b]*gs[a]-2*int(a==b)*s.eye(8))
z(chia**2-s.eye(8));z(chib**2-s.eye(8));z(Z**2-s.eye(8));z(Pe*Pe-Pe);assert Pe.rank()==4
cols=Pe.columnspace();U0=s.Matrix.hstack(*cols);z(U0.H*U0-s.eye(4));U=U0*chi4
z(U.H*U-s.eye(4));z(U*U.H-Pe);z(U.H*chia*U-chi4)
for i in range(4):z(U.H*gs[i]*U-g4[i]);z(Z*gs[i]-gs[i]*Z)
hatpairs={}
for i in range(4,6):
 z(U.H*gs[i]*U);z(Z*gs[i]+gs[i]*Z)
 for j in range(4,6):
  hp=U.H*gs[i]*gs[j]*U;hatpairs[f'{i}_{j}']=enc(hp)
  z(hp+U.H*gs[j]*gs[i]*U-2*int(i==j)*s.eye(4))
PL=(s.eye(8)+chia)/2;PR=s.eye(8)-PL;P4=[(s.eye(4)+chi4)/2,(s.eye(4)-chi4)/2];P=[PL,PR]
for g in gs:z(g*PL-PR*g);z(g*PR-PL*g)
for a,b in product(range(2),repeat=2):
 for i in range(6):z(U.H*P[a]*gs[i]*P[b]*U-(P4[a]*g4[i]*P4[b] if i<4 else s.zeros(4)))
# Arbitrary chiral charges and masses: physical restriction, no parity average.
cL,cR,M,V=s.symbols('cL cR M V',commutative=False);A=PL*cL+PR*cR;At=PR*cL+PL*cR
for g in gs:z(g*A-At*g)
z(U.H*(PL*M+PR*V)*U-(P4[0]*M+P4[1]*V))
z(PL*(cR*M-M*cL)+PR*(cL*V-V*cR)-(At*(PL*M+PR*V)-(PL*M+PR*V)*A))
x,h,eps,L=s.symbols('x h epsilon L');d=4-2*eps
F=[];Long=[]
for nh in range(3):
 frow=[];lrow=[]
 for nu in range(4):
  q=gs[nu];f=sum((t*q*t for t in gs[:4+nh]),s.zeros(8));lin=sum((x*t*q*t-2*(1-x)*q for t in gs[:4+nh]),s.zeros(8))
  fm=s.expand(U.H*f*U);lm=(U.H*lin*U).applyfunc(s.expand)
  fc=s.expand(s.trace(g4[nu]*fm)/4);lc=s.expand(s.trace(g4[nu]*lm)/4)
  z(fm-fc*g4[nu]);z(lm-lc*g4[nu]);frow.append(fc);lrow.append(lc)
 assert len(set(frow))==len(set(lrow))==1;F.append(frow[0]);Long.append(lrow[0])
fp=s.interpolate(list(enumerate(F)),h);lp=s.interpolate(list(enumerate(Long)),h)
assert s.degree(fp,h)<=1 and s.degree(lp,h)<=1
B=lambda a,b:s.gamma(a)*s.gamma(b)/s.gamma(a+b)
norm=s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)
def jf(n):return norm*B(1-eps,1-eps)*(-n)/2
def jl(n):
 # The p^3 numerator term is retained, not a Taylor residue shortcut.
 poly=s.Poly(s.expand(x*n/2),x);linear=sum(co*B(power[0]+1-eps,1-eps) for power,co in poly.terms())
 return -norm*(linear+eps*B(2-eps,2-eps))
reg={'actual_F':jf(fp.subs(h,0)),'reference_F':jf(fp.subs(h,-2*eps)),
 'actual_L':jl(lp.subs(h,0)),'reference_L':jl(lp.subs(h,-2*eps)),
 'actual_Y':norm*B(1-eps,1-eps)/2,'reference_Y':norm*B(1-eps,1-eps)/2}
def jet(f):return [str(s.simplify(f.subs(eps,0))),str(s.simplify(s.diff(f,eps).subs(eps,0)))]
jets={k:jet(v) for k,v in reg.items()}
for k in ['F','L','Y']:jets['delta_'+k]=jet(reg['actual_'+k]-reg['reference_'+k])
# Full color contractions from the actual odd-Fock matrices and H plane.
YCT=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');Ts=list(map(dec,YCT['Tminus']));H=dec(YCT['H_new']);PH=H*H.T
wh,wm=s.symbols('eta_H xi');W=wm*s.eye(45)+(wh-wm)*PH
CF=sum((t*t for t in Ts),s.zeros(16));CH=sum((v*Ts[a]*Ts[b] for (a,b),v in s.SparseMatrix(PH).todok().items()),s.zeros(16))
CW=sum((v*Ts[a]*Ts[b] for (a,b),v in s.SparseMatrix(W).todok().items()),s.zeros(16))
DG=(s.sympify(jets['delta_F'][1])*CF+s.sympify(jets['delta_L'][1])*(CW-CF)).applyfunc(s.simplify)
# Complete real scalar sums; no old FYS derived data read.
Bs=[dec(YCT[k]) for k in ['B10','B126']];bs=[[s.SparseMatrix(16,16,{(i//16,i%16):v for (i,j),v in s.SparseMatrix(b[:,a]).todok().items()}) for a in range(328)] for b in Bs]
il=[];ir=[];mix=[]
for mats in bs:il.append(sum((b.H*b for b in mats),s.zeros(16)));ir.append(sum((b*b.H for b in mats),s.zeros(16)))
for a,b in [(0,1),(1,0)]:mix.append(sum((bs[a][i].H*bs[b][i] for i in range(328)),s.zeros(16)))
ys=[s.Matrix(3,3,lambda i,j:LOC[f'u{R}_{min(i,j)}{max(i,j)}']+s.I*LOC[f'v{R}_{min(i,j)}{max(i,j)}']) for R in ['10','126']]
yl=[(y.H*y).applyfunc(s.expand) for y in ys];yr=[(y*y.H).applyfunc(s.expand) for y in ys]
WY=sum((s.kronecker_product(y,b) for y,b in zip(yl,il)),s.zeros(48));WYright=sum((s.kronecker_product(y,b) for y,b in zip(yr,ir)),s.zeros(48))
finish('primary',{'method':'projected_gamma8_dimension_polynomial_and_complete_shifted_parameter_integrals','external_embedding':enc(U),'external_projector':enc(Pe),'physical_chi':enc(chi4),'hat_pair_matrices':hatpairs,
 'Feynman_numerator_by_hat_rank':list(map(str,F)),'longitudinal_linear_numerator_by_hat_rank':list(map(str,Long)),
 'Feynman_numerator_polynomial':str(fp),'longitudinal_linear_numerator_polynomial':str(lp),'jets':jets,'exact_regular_integrals':{k:str(v) for k,v in reg.items()},
 'full_Casimir':enc(CF),'unbroken_Casimir':enc(CH),'width_Casimir':enc(CW),'gauge_finite_difference_left':enc(DG),'gauge_finite_difference_right':enc(DG.T),
 'scalar_sums_left':list(map(enc,il)),'scalar_sums_right':list(map(enc,ir)),'scalar_mixed_sums':list(map(enc,mix)),'family_left':list(map(enc,yl)),'family_right':list(map(enc,yr)),
 'Yukawa_tensor_left':enc(WY),'Yukawa_tensor_right':enc(WYright),'Yukawa_finite_difference':enc(s.zeros(48)),
 'gauge_open_phase':'-i','Yukawa_open_phase':'+i','physical_spin_rank':4,'open_line_half_or_trace_divisor':False,'extra_family_three':False,
 'full_internal_hat_vector_vertices_retained':True,'closed_odd_chi_trace_constructed':False,'physical_scheme_adopted':False,'new_two_loop_integrals':0},start)
