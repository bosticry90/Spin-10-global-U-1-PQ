"""Complete conservative contact comparison; no dense scattering compiler."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations,combinations_with_replacement
from collections import defaultdict
from fractions import Fraction as F
from math import isqrt
import json,sys,time,threading,os
import sympy as S
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_higgs_neutral_valley'));import inputs as inp
sys.path.insert(0,str(C/'canonical_so10_general_coherent_sigma'));import contract_v2 as wick
sys.path.insert(0,str(C/'canonical_so10_fixed_portal_bound'));import bound as portals
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def radical(q):
 q=F(q);den=10000;n=isqrt(q.numerator*den*den//q.denominator)
 if F(n*n,den*den)<q:n+=1
 assert F(n*n,den*den)>=q
 return F(n,den)
def q1stats(rows):
 cols=defaultdict(F);tr=F(0);rowmax=0
 for row in rows.values():
  rowmax=max(rowmax,sum(abs(a)+abs(b) for a,b in row.values()))
  for pair,(a,b) in row.items():
   w=1 if pair[0]==pair[1] else 2
   cols[pair]+=F(abs(a)+abs(b),w);tr+=F(a*a+b*b,w)
 colmax=max(cols.values());betaH=rowmax*colmax
 return {'rows':len(rows),'entries':sum(map(len,rows.values())),'trace_H':str(tr),'max_row':str(rowmax),'max_weighted_column':str(colmax),'beta_H_upper':str(betaH),'alpha':str(tr/252)}
def phi_gram():
 B=[{(i,j):1,(j,i):1} for i,j in combinations(range(10),2)]
 B +=[{**{(i,i):1 for i in range(k)},(k,k):-k} for k in range(1,10)]
 g=[sum(v*v for v in b.values()) for b in B];gram=defaultdict(F)
 for a,A in enumerate(B):
  for b,BB in enumerate(B):
   D=portals.product(A,BB)
   for ij,v in portals.product(BB,A).items():D[ij]=D.get(ij,0)+v
   for ij,u in D.items():
    for kl,v in D.items():gram[ij+kl]+=F(u*v,4*g[a]*g[b])
 for i in range(10):
  for j in range(10):
   for k in range(10):
    for l in range(10):
     expected=F(27,50)*(i==j)*(k==l)+F(14,5)*(F((i==k)*(j==l)+(i==l)*(j==k),2)-F((i==j)*(k==l),10))
     assert gram[i,j,k,l]==expected
 return B,g
def representation_gram(B,g):
 tops=[(0,)+K for K in combinations(range(1,10),4)];ix={I:a for a,I in enumerate(tops)};gram=defaultdict(F);count=0
 # All canonical chiral coefficients; R maps this chirality to its opposite.
 for A,metric in zip(B,g):
  for I in tops:
   J=tuple(i for i in range(10) if i not in I);f={I:1,J:-1j*wick.parity(I+J)};out=defaultdict(complex)
   for K,z in f.items():
    for p,old in enumerate(K):
     for (new,old0),v in A.items():
      if old0!=old:continue
      T=K[:p]+(new,)+K[p+1:]
      if len(set(T))<5:continue
      out[tuple(sorted(T))]+=v*z*wick.parity(T)
   out={K:z for K,z in out.items() if z};v={ix[K]:z for K,z in out.items() if K in ix}
   for K,z in out.items():
    L=tuple(i for i in range(10) if i not in K)
    assert out.get(L,0)==1j*wick.parity(K+L)*z
   assert len(v)<=1
   for a,u in v.items():
    norm=u.real*u.real+u.imag*u.imag;assert norm==int(norm)
    gram[a,a]+=F(int(norm),metric)
   count+=len(v)
 # Entries here are rational sums; confirm exactly with integer denominator.
 # Recompute diagonal rationally, rather than accept floating equality.
 diagonal=[F(0) for _ in tops]
 for A,metric in zip(B,g):
  if all(i==j for i,j in A):
   for a,I in enumerate(tops):diagonal[a]+=F(sum(A.get((i,i),0) for i in I)**2,metric)
  else:
   i,j=next(iter(A))
   for a,I in enumerate(tops):diagonal[a]+=F((i in I)!=(j in I),metric)
 assert set(diagonal)=={F(15)} and all(gram.get((a,b),0)==(15 if a==b else 0) for a in range(126) for b in range(126))
 # Offdiagonal generators are signed monomial matrices; diagonal ones diagonal.
 # Thus every individual R R^dagger has exactly zero offdiagonal entries.
 return {'dimension':126,'constant':'15','real_trace_square':56700,'nonzero_representation_entries':count,'exact_diagonal':list(map(str,diagonal))}
def controls():
 x=S.symbols('x0:3',real=True);A=S.Matrix([[1,2,0],[2,-1,1],[0,1,2]]);xx=S.Matrix(x);V=(xx.dot(A*xx))**2
 M,pairs=wick.geo.pairmatrix(V,x)
 for i,j in pairs:
  X=S.zeros(3);X[i,j]=X[j,i]=1 if i==j else 1/S.sqrt(2)
  Y=4*(A*S.trace(A*X)+2*A*X*A);v=S.Matrix([Y[a,b]*(1 if a==b else S.sqrt(2)) for a,b in pairs])
  assert wick.geo.zero(M[:,pairs.index((i,j))]-v)
 x,y,u,v=S.symbols('x y u v',real=True);zz=(x+S.I*y)/S.sqrt(2);ww=(u+S.I*v)/S.sqrt(2)
 E=S.expand(zz**2*S.conjugate(zz)*ww);VV=S.expand(E+S.conjugate(E));MM,pp=wick.geo.pairmatrix(VV,[x,y,u,v]);assert sum(a*a for a in MM)==24
 C0=S.Matrix([[1,2],[2,3]]);W=S.expand((S.Matrix([x,y]).dot(C0*S.Matrix([x,y])))*(u*u+2*v*v))
 MM,pp=wick.geo.pairmatrix(W,[x,y,u,v]);pX=[i for i,(a,b) in enumerate(pp) if b<2];pY=[i for i,(a,b) in enumerate(pp) if a>=2];pXY=[i for i,(a,b) in enumerate(pp) if a<2<=b]
 n=S.trace(C0.T*C0)*5;assert sum(a*a for a in MM.extract(pX,pY))==4*n and sum(a*a for a in MM.extract(pXY,pXY))==16*n
 return {'SOS_action_fourth_derivatives':True,'eta_real_Frobenius_factor12_Fock':True,'mixed_direct4_crossed16':True,'wrong_identical_or_realification_changes':24!=12,'whole_upper_not_lower':True}
def main():
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();prep=read(O/'preparation.json');writes=[]
 def readonly(event,args):
  if event=='open' and len(args)>1 and isinstance(args[1],str) and any(t in args[1] for t in 'wax+'):
   writes.append(str(args[0]));raise PermissionError('CONTACT_WRITE_DENIED')
 sys.addaudithook(readonly)
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 forms=[]
 for a,tail in enumerate(combinations(range(1,10),4)):
  I=(0,)+tail;J=tuple(i for i in range(10) if i not in I);forms.extend([(I,a,(1,0)),(J,a,(0,-wick.parity(I+J)))])
 stats=q1stats(wick.build_rows(1,forms));print('STAGE complete_Q1_Schur_and_trace',flush=True)
 Bphi,gphi=phi_gram();rep=representation_gram(Bphi,gphi);ct=controls()
 point=read(C/'canonical_so10_coherent_joint_witness/POINT.json');p1,p2,x,s,z,D,t,eta=[F(point[n]) for n in ['p1','p2','x','s','z','D','t','eta']];assert F(point['Delta'])==0
 p5=x/8;p7=(-3*s-z)/2+5*D/24;p8=(z-s)/4
 q1=4*(F(stats['beta_H_upper'])/2+2*F(stats['alpha']));q4=4*(70+2*30)
 sigma=4*254*p5+(abs(s)+4*abs(p8))*q1+abs(p7)*q4
 phi=4*56*p1+abs(p2)*4*(F(27,5)+2*F(29,10))
 old=read(C/'canonical_so10_fixed_portal_bound/primary_result.json');m4=read(C/'canonical_so10_fixed_mixed_screen/primary_result.json');ep=read(C/'canonical_so10_eta_offdiagonal_bound/primary_result.json')
 co={n:F(v) for n,v in old['canonical_coefficients'].items()};dims=[1485,31878,210,3,13608,1080,108,5040,504,40];assert sum(dims)==53956
 B=[[F(0) for j in range(10)] for i in range(10)]
 def edge(i,j,v):B[i][j]+=v;B[j][i]+=v
 B[0][0]=phi;B[1][1]=sigma;B[2][2]=22*abs(co['lambdaPhiVector1'])+20*abs(co['lambdaPhiVector2']);B[3][3]=4*abs(co['lambdaS'])
 direct=t*radical(56700);edge(0,1,direct);B[4][4]=2*direct
 for i,j,k,key in [(0,2,5,'Phi_portal_real_operator_Frobenius_squared'),(1,2,7,'Sigma_portal_real_operator_Frobenius_squared')]:
  sq=F(old[key]);e=radical(sq/6);edge(i,j,e);B[k][k]=2*e
 h=abs(co['lambdaVectorS']);edge(2,3,h*radical(10));B[9][9]=h
 edge(1,7,eta*radical(6*ep['charged_Fock_trace_eta_stripped']))
 assert F(m4['selected_operator_norm_squared'])<F(49,100);Z=F(7,10)
 w=list(map(F,['1/4','1','1/5','1/500','1','1','1/25','1/50','1/10','1/5']))
 rows=[sum(a*b for a,b in zip(row,w))/wi for row,wi in zip(B,w)];up=max(rows)+Z
 inv=read(C/'canonical_so10_fixed_mixed_screen/primary_result.json')['action_quartic_field_inventory'];names=[n for n in inp.NAMES if inp.TOTAL[n]==4];assert len(names)==22 and names==[v['name'] for v in inv]
 zero=['lambdaPhiS','lambdaSigmaS','zD'];fixed=inp.coefficients(0);assert all(fixed[n]==0 for n in zero)
 for n,hv in prep['input_sha256'].items():assert digest(R/n)==hv,n
 assert not writes and time.perf_counter()-start<120
 out={'schema':'COMPLETE_CONTACT_UPPER_PRIMARY_V1','status':'COMPLETE_BOUND_REQUIRE_INDEPENDENT_RECEIPT','Q1_stats':stats,'Q1_unit_operator_upper':str(q1),'Q4_unit_operator_upper':str(q4),'Sigma_full_operator_upper':str(sigma),'Phi_full_operator_upper':str(phi),'representation_Gram':rep,'pair_dimensions':dims,'all22_quartic_names':names,'zero_quartics':zero,'comparison_matrix':[[str(a) for a in row] for row in B],'positive_weights':list(map(str,w)),'weighted_row_bounds':list(map(str,rows)),'complete_Z_upper':str(Z),'complete_M_upper':str(up),'complete_a0_upper_expression':str(up)+'/16/pi','complete_a0_upper_decimal':str(S.N(S.Rational(up.numerator,up.denominator)/(16*S.pi),20)),'complete_contact_pass_upper':up<8*F(157,50),'pi_lower_used':'157/50','physical_compression_bounded':True,'full_gauged_amplitude_qualified':False,'full328_BFB_proved':False,'quantum_control_proved':False,'new_points':0,'new_benchmark_adopted':False,'scientific_authority_changed':False,'whole_goal_complete':False,'controls':ct,'seconds_after_import':time.perf_counter()-start,'input_sha256':prep['input_sha256'],'write_attempts':writes}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True);timer.cancel()
if __name__=='__main__':main()
