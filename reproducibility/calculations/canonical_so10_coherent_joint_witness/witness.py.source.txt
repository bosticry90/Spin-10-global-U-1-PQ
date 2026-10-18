"""One frozen rational necessary-set fixture with exact outward sign certificates."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import json,sys,time,threading,os
import sympy as S
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_higgs_exact_quartic_transport'));import transport as qt
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
P=S.symbols('p1:9',real=True);m=S.Symbol('m',real=True);eta=S.Symbol('eta',real=True);h=S.symbols('h0:8',real=True);rho=S.Symbol('rho',positive=True)
loc={**dict(zip(map(str,P),P)),**dict(zip(map(str,h),h)),'m':m,'eta':eta}
parse=lambda a:S.sympify(a,locals=loc)
matrix=lambda A:S.Matrix([[parse(a) for a in row] for row in A])
clean=lambda A:A.applyfunc(lambda a:S.simplify(S.expand(a)))
def zero(a):
 if isinstance(a,S.MatrixBase):return all(zero(v) for v in a)
 return S.expand(a)==0 or S.simplify(S.cancel(a))==0
def main():
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();writes=[]
 def readonly(event,args):
  if event=='open' and len(args)>1 and isinstance(args[1],str) and any(v in args[1] for v in 'wax+'):
   writes.append(str(args[0]));raise PermissionError('JOINT_WITNESS_WRITE_DENIED')
 sys.addaudithook(readonly)
 prep=read(O/'preparation.json')
 for n,v in prep['input_sha256'].items():assert digest(R/n)==v,n
 pt=read(O/'POINT.json');p1,p2,x,s,z,D,t,Delta,e=[S.Rational(pt[n]) for n in ['p1','p2','x','s','z','D','t','Delta','eta']]
 vals=[p1,p2,Delta+t/4,t,x/8,(5*s+z)/2-5*D/24,(-3*s-z)/2+5*D/24,(z-s)/4];sub=dict(zip(P,vals));sub[eta]=e
 src=read(C/'canonical_so10_eta_variable_inputs/primary_result.json')
 block=lambda name,key:clean(matrix(src['blocks'][name][key]).subs(sub))
 SW=block('weak','Sigma_principal');SC=block('colored','Sigma_principal');BW=e*block('weak','eta_stripped_mixing');BC=e*block('colored','eta_stripped_mixing');FW=block('weak','phi_constant');FC=block('colored','phi_constant')
 KW=clean(BW.H*SW.inv()*BW-FW);KC=clean(BC.H*SC.inv()*BC-FC)
 top=lambda K:S.trace(K)/2+S.sqrt(S.expand(((K[0,0]-K[1,1])/2)**2+K[0,1]*K[1,0]))
 mW,mC=top(KW),top(KC)
 Hraw=matrix(src['raw_H8']).subs(sub);HS=Hraw[:4,:4];mix=Hraw[:4,4:];invHS=clean(HS.inv());F4=clean((Hraw[4:,4:].subs(m,0)-mix.T*invHS*mix)/2)
 assert all(F4[i,j]==0 for i in [0,3] for j in [1,2])
 F2=F4.extract([0,3],[0,3]);mean=S.trace(F2)/2;a=S.expand((F2[0,0]-F2[1,1])/2);b=F2[0,1];rho2=S.expand(a*a+b*b);root=rho-mean
 assert zero((F4-mean*S.eye(4))**2-rho2*S.eye(4)) and zero(S.trace(KW)/2+mean)
 assert zero(S.expand(((KW[0,0]-KW[1,1])/2)**2+KW[0,1]*KW[1,0])-rho2)
 phi=S.Matrix([-b/(rho+a),0,0,1]);hv=(-invHS*mix*phi).col_join(phi)
 def modzero(v):
  if isinstance(v,S.MatrixBase):return all(modzero(a) for a in v)
  num=S.cancel(v).as_numer_denom()[0];rem=S.rem(S.Poly(num,rho),S.Poly(rho*rho-rho2,rho)).as_expr();return zero(rem)
 assert modzero(Hraw.subs(m,root)*hv)
 g8=list(map(S.Rational,src['raw_neutral8_metric']));N=S.expand((hv.T*S.diag(*g8)*hv)[0])
 qt.GRID=10**100
 def atan(d):
  a=sum(((-1)**j*F(1,(2*j+1)*d**(2*j+1)) for j in range(80)),F());return a,a+F(1,161*d**161)
 ap,bp=atan(5),atan(239);pii=qt.I(16*ap[0]-4*bp[1],16*ap[1]-4*bp[0])
 def iv(v,atoms=None):
  v=S.sympify(v)
  if atoms and v in atoms:return atoms[v]
  if v==S.pi:return pii
  if v==rho:return iv(rho2).sqrt()
  if v.is_Rational:return qt.I(F(str(v)))
  if v.is_Add:return sum((iv(a,atoms) for a in v.args),qt.I())
  if v.is_Mul:
   ans=qt.I(1)
   for a in v.args:ans*=iv(a,atoms)
   return ans
  assert v.is_Pow,(v,v.func)
  base,pow=v.args
  if pow==S.Rational(1,2):return iv(base,atoms).sqrt()
  assert pow.is_Integer,v
  ans=qt.I(1)
  for _ in range(abs(int(pow))):ans*=iv(base,atoms)
  return ans if pow>=0 else 1/ans
 HI=[iv(v) for v in hv];hatoms=dict(zip(h,HI));NI=sum((v.square()*gg for v,gg in zip(HI,g8)),qt.I());assert NI.lo>0
 H10=matrix(src['raw_H10']).subs(sub);ids=src['positive_neutral_indices'];Hp=H10.extract(ids,ids);HPI=[[iv(v) for v in row] for row in Hp.tolist()]
 _,pivots=qt.ldl(HPI)
 jforms=[S.expand(parse(v).subs(sub)) for v in src['raw_j_forms']];js=[iv(v,hatoms) for v in jforms];j=[js[i] for i in ids]
 # Exact Ward/kernel consequences, not assigning phase-zero propagators.
 hsub=dict(zip(h,hv))
 for i in [2,4]:assert modzero(jforms[i].subs(hsub,simultaneous=True))
 V4=S.expand(parse(src['direct_V4']).subs(sub));direct=4*iv(V4,hatoms)/NI.square();exchange=2*qt.dot(j,qt.solve(HPI,j))/NI.square();lam=direct-exchange
 print('STAGE actual_weak_kernel_full_neutral_relaxation',flush=True)
 c0=-S.Rational(2347941,50000000)*S.sqrt(15);c2=S.Rational(2070819875283,10**13);n0=S.Rational(6212459625849,2500000000000000);q=25*t
 A7=S.Matrix([[q+24*z/5,SW[0,1]],[SW[1,0],q+24*s/5+12*z/5]]);B2=S.Matrix([[q,SW[0,1]],[SW[1,0],q+D]])
 Fphi=480*p1+56*p2+c0;L=3*x/5;AT=80*p2+3*t/10+5*c0;AC=20*p2+3*t/10-5*c0
 mass={'z_type':24*z/5,'sz_type':12*(2*s+z)/5,'Phi_triplet':80*p2+5*c0,'Phi_octet':20*p2-5*c0,'radial_F':Fphi,'radial_L':L,'radial_det':Fphi*L-(24*Delta)**2,'singlet':S.Rational(6,5),'mixed_Phi_triplet_diagonal':AT,'mixed_Phi_triplet_det':AT*D-n0,'mixed_Phi_sextet_diagonal':AC,'mixed_Phi_sextet_det':AC*D-n0,'mW_minus_mC':mW-mC,'weak_root_gap':2*S.sqrt(rho2)}
 for name,A in [('SW',SW),('SC',SC),('A7',A7),('B2',B2)]:
  for k in range(1,A.rows+1):mass[name+'_minor_'+str(k)]=S.simplify(S.expand(A[:k,:k].det()))
 massI={n:iv(v) for n,v in mass.items()};masspass=all(v.lo>0 for v in massI.values())
 mu=read(C/'canonical_so10_general_coherent_sigma/validation_receipt.json');ls={str(a):v for a,v in [('x',x),('s',s),('z',z),('D',D)]};ell=S.sympify(mu['ell_x_s_z_D']).subs(ls)
 contact={'coherent':S.pi/112-ell,'Sigma_ellipse':256*S.pi**2-50*(x+16*z)**2-36*(x+16*s+8*z)**2,'Sigma_diag0':16*S.pi-abs(3*x),'Sigma_diag1':16*S.pi-abs(3*x+24*z),'Sigma_diag2':16*S.pi-abs(3*x+24*(z-s)+5*D),'Phi_plus':16*S.pi-abs(32*p1+6*p2),'Phi_minus':16*S.pi-abs(16*p1+6*p2)}
 Lambda=p1+7*p2/60
 rays={'Phi_min':p1+p2/10,'Phi_max':p1+73*p2/90,'Lambda':Lambda,'Sigma1':x/8,'mixed_radial':Delta+2*S.sqrt(Lambda*x/8)}
 hc=S.Rational(199571,1562500);kc=-S.Rational(9356043,50000000);gc=S.Rational(2,5);cc=9*x/2-27*s+33*z+35*D/4
 slices={'uniform_A':48*x+960*s-147456*e*e/hc,'uniform_B':cc-kc*kc/gc-18*e,'uniform_r4':3*gc/4-6*e,'W1':361*x/2+933*s+33*z+35*D/4+S.Rational(497030229,2000000)-3960*e,'W2':8281*x/162+S.Rational(1199,3)*s+33*z+35*D/4+S.Rational(2821340701,28125000)-S.Rational(4384,3)*e}
 z4sq=S.Rational(690273291761,400000000000000)
 bfb={'pure_Sigma1':x/8,'pure_Sigma3':vals[6],'pure_Sigma_cone':s-2*vals[7],'Phi_lower':p1+p2/10,'positive_t':t,'Sigma_Schur_308':x/8-z4sq*z4sq/(t*t)}
 extra={**contact,**rays,**slices,**bfb};extraI={n:iv(v) for n,v in extra.items()};extra_pass=all(v.lo>0 for v in extraI.values())
 width=lam.hi-lam.lo;assert width<F('1e-30')
 passed=masspass and extra_pass and lam.lo>0
 wrongNI=sum((v.square() for v in HI),qt.I());assert (NI-wrongNI).lo>0
 assert (direct-exchange/2-lam).lo>0 and 3*S.Rational(1,10)>e
 for n,v in prep['input_sha256'].items():assert digest(R/n)==v,n
 assert not writes and time.perf_counter()-start<120
 view=lambda v:[str(S.N(S.Rational(a.numerator,a.denominator),23)) for a in [v.lo,v.hi]]
 out={'schema':'COHERENT_JOINT_WITNESS_PRIMARY_V1','status':'LISTED_JOINT_CONDITIONS_PASS_REQUIRE_INDEPENDENT_RECEIPT' if passed else 'FROZEN_POINT_NEGATIVE_OR_INCONCLUSIVE_REQUIRE_VERIFIER','parameter_values':{str(a):str(v) for a,v in sub.items()},'physical_mass_pattern_if_pass':[290,38],'local_mass_conditions_pass':bool(masspass),'mass_expressions':{n:str(v) for n,v in mass.items()},'mass_intervals':{n:v.dump() for n,v in massI.items()},'other_predicates_pass':bool(extra_pass),'other_expressions':{n:str(v) for n,v in extra.items()},'other_intervals':{n:v.dump() for n,v in extraI.items()},'coherent_ell':str(ell),'coherent_abs_expectation':str(56*ell/S.pi),'mW_interval':iv(mW).dump(),'mC_interval':iv(mC).dump(),'mass_gap_view':view(iv(mW-mC)),'root_rho_squared':str(rho2),'weak_kernel_raw':list(map(str,hv)),'weak_kernel_exact_mod_root_checked':True,'phase_source_zeros_exact':True,'light_norm_interval':NI.dump(),'direct_quartic_interval':direct.dump(),'exchange_interval':exchange.dump(),'lambda_interval':lam.dump(),'lambda_interval_view':view(lam),'lambda_width_qualified':True,'relaxed_quartic_positive':bool(lam.lo>0),'neutral_heavy_raw':[[str(v) for v in row] for row in Hp.tolist()],'positive_neutral_pivots':[v.dump() for v in pivots],'pure252_and_restricted308_BFB':bool(all(extraI[n].lo>0 for n in bfb)),'full328_BFB_proved':False,'complete_contact_perturbativity_pass':False,'full_gauged_scattering_pass':False,'quantum_control_proved':False,'new_exploratory_points':1,'optimizer_or_parameter_search':False,'new_benchmark_adopted':False,'physical_inputs_adopted':False,'old_curve_reopened':False,'scientific_authority_changed':False,'whole_goal_complete':False,'input_sha256':prep['input_sha256'],'state_sha256':prep['state_sha256'],'write_attempts':writes}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True);timer.cancel()
if __name__=='__main__':main()
