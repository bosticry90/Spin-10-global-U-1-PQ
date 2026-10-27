"""OFK1 exterior words, unshifted numerator identities and Schwinger/IBP."""
from data import *
from itertools import product
start=begin('replay')
def zero(M):assert not s.SparseMatrix(M).applyfunc(s.expand).todok()
# Independent bitmask exterior-Clifford multiplication, no gamma8 arithmetic.
def cm(a,b):return (-1)**sum((b&((1<<i)-1)).bit_count() for i in range(6) if a&(1<<i)),a^b
def mul(A,B):
 out={}
 for a,v in A.items():
  for b,w in B.items():sg,k=cm(a,b);out[k]=s.expand(out.get(k,0)+sg*v*w)
 return {k:v for k,v in out.items() if v!=0}
def sub(A,B):return {k:v for k in set(A)|set(B) if (v:=s.expand(A.get(k,0)-B.get(k,0)))!=0}
k=s.symbols('k0:6');p=s.Symbol('p');K={1<<i:k[i] for i in range(6)};Kb={1<<i:k[i] for i in range(4)};P={1:p};R=sub(P,K);Rb=sub(P,Kb)
full=mul(mul(K,R),K);bar=mul(mul(Kb,Rb),Kb)
# Triple same-vector identity removes all grade3 words before projection.
assert all(mask.bit_count()==1 for mask in full)
projected={m:v for m,v in full.items() if m<16}
diff=sub(bar,projected);hat2=k[4]**2+k[5]**2
target={mask:s.expand(hat2*(coef+P.get(mask,0))) for mask,coef in Kb.items()}
assert not sub(diff,target)
for i in range(6):
 sg,m=cm(63,1<<i);sg2,m2=cm(1<<i,63);assert m==m2 and sg==-sg2
# Tensor-factor construction of the physical injection, independently chosen.
sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1)
phys=[s.kronecker_product(sy,t) for t in [sx,sy,sz]]+[s.kronecker_product(sx,s.eye(2))];ch=s.prod(phys)
down=s.Matrix([0,1]);U=s.kronecker_product(ch,down);Pe=s.kronecker_product(s.eye(4),(s.eye(2)-sz)/2)
zero(U.H*U-s.eye(4));zero(U*U.H-Pe)
for g in phys:zero(U.H*s.kronecker_product(g,sz)*U-g)
zero(U.H*(-s.kronecker_product(ch,sz))*U-ch)
# Exact off-shell reference reduction. In N_L=2(k.r)k-k^2 r,
# 2k.r=p^2-k^2-r^2. The odd integral k/k^4 vanishes in this symmetric
# dimensional prescription; p^2*integral k/(k^4 r^2)=eps*p*J.
eps,L,h=s.symbols('epsilon L h');d=4-2*eps
B=lambda a,b:s.gamma(a)*s.gamma(b)/s.gamma(a+b)
regJ=s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)*B(1-eps,1-eps)
refF=(d-2)*regJ/2;refL=(1-eps)*regJ
assert s.simplify(refF-refL)==0
# Schwinger hat Gaussian moment: <hat k^2>=h/(2s).
# It multiplies bar k+p, whose shifted mean is (2-x)p, with weight2x.
# This integrates the actual unshifted difference, not just its UV pole.
delF=-h*regJ/2
delL=-h*s.exp((s.EulerGamma+L)*eps)*s.gamma(1+eps)*(2*B(2-eps,1-eps)-B(3-eps,1-eps))/2
reg={'reference_F':refF,'reference_L':refL,'actual_F':refF+delF.subs(h,-2*eps),'actual_L':refL+delL.subs(h,-2*eps),
 'actual_Y':regJ/2,'reference_Y':regJ/2}
def jet(f):return [str(s.simplify(f.subs(eps,0))),str(s.simplify(s.diff(f,eps).subs(eps,0)))]
jets={name:jet(v) for name,v in reg.items()}
for a in ['F','L','Y']:jets['delta_'+a]=jet(reg['actual_'+a]-reg['reference_'+a])
# Wrong h continuation is explicitly recomputed for a sensitive control.
wrong={'F':jet(delF.subs(h,2*eps)),'L':jet(delL.subs(h,2*eps))}
D=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz');Ts=list(map(dec,D['Tminus']));CF=s.eye(16)*sum(s.conjugate(v)*v for t in Ts for v in t.todok().values())/16
spec={'Q':(s.Rational(4,3),s.Rational(3,4)),'uc':(s.Rational(4,3),0),'dc':(s.Rational(4,3),0),'L':(0,s.Rational(3,4)),'ec':(0,0),'N':(0,0)}
CH=s.diag(*[s.simplify(sum(spec[r['species']])+s.Rational(3,5)*s.sympify(r['Y'])**2) for r in D['SM_states']]);wh,wm=s.symbols('eta_H xi');CW=wh*CH+wm*(CF-CH)
DG=(s.sympify(jets['delta_F'][1])*CF+s.sympify(jets['delta_L'][1])*(CW-CF)).applyfunc(s.expand)
Bs=[dec(D[n]) for n in ['B10','B126']];norms=[s.simplify(sum(s.conjugate(v)*v for v in b.todok().values())) for b in Bs]
support=[{j for i,j in b.todok()} for b in Bs];assert not support[0]&support[1]
il=[s.eye(16)*v/16 for v in norms];ys=[]
for Rr in ['10','126']:
 y=s.zeros(3)
 for i in range(3):
  for j in range(i,3):y[i,j]=y[j,i]=LOC[f'u{Rr}_{i}{j}']+s.I*LOC[f'v{Rr}_{i}{j}']
 ys.append(y)
yl=[s.Matrix(3,3,lambda i,j:s.expand(sum(s.conjugate(y[a,i])*y[a,j] for a in range(3)))) for y in ys]
yr=[s.Matrix(3,3,lambda i,j:s.expand(sum(y[i,a]*s.conjugate(y[j,a]) for a in range(3)))) for y in ys]
WY=s.Matrix(48,48,lambda i,j:s.expand(sum(yl[a][i//16,j//16]*il[a][i%16,j%16] for a in range(2))))
WR=s.Matrix(48,48,lambda i,j:s.expand(sum(yr[a][i//16,j//16]*il[a][i%16,j%16] for a in range(2))))
finish('replay',{'method':'exterior_Clifford_unshifted_difference_and_Schwinger_IBP_offshell_integrals','external_embedding':enc(U),'external_projector':enc(Pe),'physical_chi':enc(ch),
 'unshifted_longitudinal_difference':{str(m):str(v) for m,v in sorted(diff.items())},'jets':jets,'exact_regular_integrals':{a:str(v) for a,v in reg.items()},'wrong_hat_dimension_sign_jets':wrong,
 'full_Casimir':enc(CF),'unbroken_Casimir':enc(CH),'width_Casimir':enc(CW),'gauge_finite_difference_left':enc(DG),'gauge_finite_difference_right':enc(DG.T),
 'scalar_sums_left':list(map(enc,il)),'scalar_sums_right':list(map(enc,il)),'scalar_mixed_sums':[enc(s.zeros(16)),enc(s.zeros(16))],
 'family_left':list(map(enc,yl)),'family_right':list(map(enc,yr)),'Yukawa_tensor_left':enc(WY),'Yukawa_tensor_right':enc(WR),'Yukawa_finite_difference':enc(s.zeros(48)),
 'scalar_isometric_norms':list(map(str,norms)),'scalar_support_sizes':list(map(len,support)),
 'gauge_open_phase':'-i','Yukawa_open_phase':'+i','physical_spin_rank':4,'open_line_half_or_trace_divisor':False,'extra_family_three':False,
 'full_internal_hat_vector_vertices_retained':True,'closed_odd_chi_trace_constructed':False,'physical_scheme_adopted':False,'new_two_loop_integrals':0},start)
