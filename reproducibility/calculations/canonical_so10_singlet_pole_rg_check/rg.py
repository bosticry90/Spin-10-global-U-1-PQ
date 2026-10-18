"""Exact S-dependent UV projection and singlet-pole RG identities at fixed inputs."""
from pathlib import Path
from hashlib import sha256
import sys,json,time,threading,os
import sympy as S
import mpmath as mp
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_higgs_neutral_valley'));import inputs as inp
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def main():
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();prep=read(O/'preparation.json');writes=[]
 def readonly(event,args):
  if event=='open' and len(args)>1 and isinstance(args[1],str) and any(t in args[1] for t in 'wax+'):
   writes.append(str(args[0]));raise PermissionError('SINGLET_RG_WRITE_DENIED')
 sys.addaudithook(readonly)
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 scalar=read(C/'canonical_so10_finite_radial_control/primary_result.json');cache=read(C/'canonical_so10_singlet_tadpole/original_v2_result.json');slots=cache['slots'];raw={n:S.sympify(v) for n,v in scalar['raw_coefficients'].items()};physical={n:S.sympify(v) for n,v in scalar['physical_parameters'].items()}
 assert physical['lambdaPhiS']==physical['lambdaSigmaS']==0 and physical['lambdaS']==1
 co=[S.im(raw[n]) if part=='im' else S.re(raw[n]) for q in slots for n,_,part in [q.partition(':')]];a,b=S.symbols('a b',real=True);u1=u2=u3=u4=S.S.Zero;trME=trDD=trMD=S.S.Zero;rows=[];coverage=0;Gs=S.Rational(3,5)
 def external(q):return [int(q=='Phi'),int(q in ['Sigma','SigmaBar']),int(q in ['phi','phiBar']),int(q in ['S','SBar'])]
 for bb in cache['block_inputs']:
  n=len(bb['metric']);rawM=[S.zeros(n) for _ in range(3)]
  for k,i,j,z in bb['raw_H34_sparse']:
   name=slots[k].partition(':')[0];p=inp.PHI[name];sig=inp.RESCALE.get(name,(0,0))[0];ss=inp.SDEG[name];degree=[p,sig,inp.TOTAL[name]-p-sig-ss,ss];ex,ey=external(bb['sectors'][i]),external(bb['sectors'][j]);remaining=[x-y-z for x,y,z in zip(degree,ex,ey)]
   assert min(remaining)>=0 and remaining[2]==0 and remaining[3]<=2
   rawM[remaining[3]][i,j]+=co[k]*S.sympify(z)*a**remaining[0]*b**remaining[1]
  for M in rawM:assert (M-M.H).applyfunc(S.simplify)==S.zeros(n)
  W=S.diag(*[1/S.Rational(g) for g in bb['metric']]);M0,M1,M2=[W*M for M in rawM];weight=bb['dimension'];local2=S.expand(weight*(S.trace(M0*M2)+S.trace(M1*M1)/2));local4=S.expand(weight*S.trace(M2*M2)/2)
  u1+=weight*S.trace(M0*M1);u2+=local2;u3+=weight*S.trace(M1*M2);u4+=local4
  M=(M0+M1+M2).subs({a:1,b:1});D=(M1+2*M2).subs({a:1,b:1});E=(2*M2).subs({a:1,b:1})
  trME+=weight*S.trace(M*E)/Gs;trDD+=weight*S.trace(D*D)/Gs;trMD+=weight*S.trace(M*D)/Gs # =Tr(M*Dcanonical)/v
  rows.append({'label':bb['label'],'real_dimension':weight*n,'c2_UV':str(S.factor(local2)),'c4_UV':str(S.factor(local4))});coverage+=weight*n
 assert coverage==328 and len(rows)==35;assert S.simplify(u1)==S.simplify(u3)==0
 u2=S.Poly(S.expand(u2),a,b);assert set(u2.monoms())=={(0,0),(2,0),(0,2)};u4=S.simplify(u4);assert not u4.has(a,b)
 bm=S.simplify(u2.coeff_monomial(1)/S.Rational(3,10));bp=S.simplify(u2.coeff_monomial(a*a)/18);bs=S.simplify(u2.coeff_monomial(b*b)/S.Rational(9,50));bl=S.simplify(u4/S.Rational(9,100));P=S.simplify(bm+60*bp+Gs*bs)
 trME,trDD,trMD=map(S.simplify,[trME,trDD,trMD]);assert S.simplify(trME+trDD-P-3*Gs*bl)==0 and S.simplify(trMD-P-Gs*bl)==0
 Ki=S.simplify(-trME-trDD);Kt=S.simplify(3*trMD);K=S.simplify(Ki+Kt);bt=-2*P;assert S.simplify(K+bt)==0
 assert S.simplify(Ki+bt)!=0 and S.simplify(K-2*bm)!=0
 singlet=read(C/'canonical_so10_singlet_quartic_running/validation_receipt.json');assert bl==S.Rational(singlet['one_loop_beta_I_at_same_point'])
 mp.mp.dps=100;num=lambda z:mp.mpf(str(S.N(z,115)));text=lambda z:mp.nstr(z,65)
 pole=read(C/'canonical_so10_singlet_pole_control/validation_receipt.json');base=mp.mpc(*map(mp.mpf,pole['formal_pole_squared']));delta=mp.mpc(*map(mp.mpf,pole['total_delta_pole_squared']));grid=[]
 for ratio in [mp.mpf('.5'),mp.mpf(1),mp.mpf(2)]:
  L=mp.log(ratio);d=delta+num(K)*L/(16*mp.pi**2);tree=mp.mpf(6)/5+num(bt)*L/(16*mp.pi**2);total=tree+d;assert abs(total-base)<mp.mpf('1e-58');grid.append({'Q_over_Q0':text(ratio),'fixed_input_delta_squared':[text(mp.re(d)),text(mp.im(d))],'formal_companion_tree_squared':text(tree),'formal_compensated_pole_squared':[text(mp.re(total)),text(mp.im(total))],'absolute_delta_over_original_tree_mass_squared':text(abs(d)/(mp.mpf(6)/5))})
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 assert not writes and time.perf_counter()-start<120
 out={'schema':'SINGLET_POLE_RG_PRIMARY_V1','status':'EXACT_LOCAL_UV_AND_POLE_LOG_IDENTITIES_REQUIRE_INDEPENDENT_RECEIPT','all35_blocks_328_real':True,'S_odd_UV_terms_exact_zero':True,'UV_c2_polynomial':str(u2.as_expr()),'UV_c4_coefficient':str(u4),'per_block_UV':rows,'beta_I':{'mS2':str(bm),'lambdaPhiS':str(bp),'lambdaSigmaS':str(bs),'lambdaS':str(bl)},'beta_I_numeric':{n:text(num(v)) for n,v in [('mS2',bm),('lambdaPhiS',bp),('lambdaSigmaS',bs),('lambdaS',bl)]},'beta_P_I':str(P),'TrME':str(trME),'TrD2':str(trDD),'TrMD_over_v':str(trMD),'explicit_log_1PI_I':str(Ki),'explicit_log_source_I':str(Kt),'explicit_log_complete_I':str(K),'tree_mass_beta_I':str(bt),'exact_RG_remainder':'0','explicit_log_derivative_numeric':text(num(K)/(16*mp.pi**2)),'zero_portals_RG_invariant_at_point':bool(bp==bs==0),'omitted_portals_remainder_I':str(S.simplify(K-2*bm)),'omitted_source_remainder_I':str(S.simplify(Ki+bt)),'scale_grid':grid,'general_nonzero_portal_beta_functions_claimed':False,'finite_RG_trajectory_computed':False,'physical_scale_optimized_or_adopted':False,'two_loop_error_bound':None,'large_pole_warning_removed':False,'new_parameter_points':0,'flavor_work_resumed':False,'scientific_authority_changed':False,'whole_goal_complete':False,'seconds_after_import':time.perf_counter()-start,'input_sha256':prep['input_sha256'],'write_attempts':writes}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True);timer.cancel()
if __name__=='__main__':main()
