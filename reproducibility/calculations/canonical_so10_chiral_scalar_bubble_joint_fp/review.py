from pathlib import Path
from hashlib import sha256
import gzip,json,time,threading,os,sympy as s,mpmath as mp
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'review_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
e,c,mu,q,t=s.symbols('epsilon c muR2 q t',positive=True);N=s.exp(s.EulerGamma*e)*mu**e;L=2**e/(1-e);S=(1-N*c**e*L)/e;assert s.simplify(s.diff(S,c)+N*c**(e-1)*L)==0
xx=s.Symbol('x',real=True);flow0=-2/c*s.integrate(s.exp(-c*q*xx),(xx,s.Rational(1,2),1));oldflow=-(s.exp(-t*q)-s.exp(-2*t*q))/(t*t*q);assert s.simplify(2*flow0.subs(c,2*t)-oldflow)==0
v=s.Symbol('v',nonnegative=True);f=1-s.exp(-v);assert f.subs(v,0)==0 and s.simplify(s.diff(v-f,v)-f)==0
beta=s.Symbol('beta_fin',real=True);coef=(s.log(mu/q)+2+beta)/3-s.Rational(1,9);assert s.diff(coef,beta)==s.Rational(1,3) and s.simplify(q*s.diff(coef,q))==-s.Rational(1,3)
assert s.simplify(s.limit(N*c**e*(L-1)/e,e,0))==s.log(2)+1
load=lambda p:json.loads(gzip.decompress(p.read_bytes()));rows=load(O/'primary_tables.json.gz')['rows'];F=load(O.parent/'canonical_so10_chiral_transverse_joint_limit/primary_tables.json.gz')['rows'];J=load(O.parent/'canonical_so10_chiral_joint_heat_pilot/primary_v2_tables.json.gz');mp.mp.dps=100;controls={'wrong_complete_subtraction_sign':0,'omit_explicit_lower_face_positive_epsilon':0,'separate_lower_face_e0_not_evaluated':0,'fixed_face_changes_subtraction':0,'omit_transverse_transport':0,'erase_nonzero_Ward_contact':0};minfaces=None
for idx,(r,ff) in enumerate(zip(rows,F)):
 ev,qv,muv=mp.mpf(r['epsilon']),mp.mpf(r['q']),mp.mpf('1.5');cv=mp.mpf(r['cq'])/qv if r['kind']=='finite' else mp.exp(-mp.mpf(r['a'])/ev)/qv;nv=mp.exp(mp.euler*ev)*muv**ev;sv=mp.mpf(r['S']);controls['wrong_complete_subtraction_sign']+=int(2*sv!=0)
 if ev:
  lower=nv*cv**ev*2**ev/((1-ev)*ev);assert lower!=0;controls['omit_explicit_lower_face_positive_epsilon']+=1
 else:controls['separate_lower_face_e0_not_evaluated']+=1
 df=(nv*cv**ev*(2**ev/(1-ev)-1)/ev) if ev else mp.log(2)+1;assert abs(df)>mp.mpf('1e-40');controls['fixed_face_changes_subtraction']+=1;minfaces=abs(df) if minfaces is None else min(minfaces,abs(df));controls['omit_transverse_transport']+=int(mp.mpf(ff['boundary_transport'])!=0);wr=mp.mpf(J['numeric_kernels'][idx]['Ward_power_subtracted']) if idx<9 else mp.mpf(J['correlated_paths'][idx-9]['Ward_ren']);controls['erase_nonzero_Ward_contact']+=int(wr!=0)
assert controls=={'wrong_complete_subtraction_sign':18,'omit_explicit_lower_face_positive_epsilon':15,'separate_lower_face_e0_not_evaluated':3,'fixed_face_changes_subtraction':18,'omit_transverse_transport':18,'erase_nonzero_Ward_contact':18}
receipt=read(O/'validation_receipt.json');assert receipt['uniform_scalar_and_full_selected_quadratic_comparison_constructed'] and receipt['tensor_positions_with_inherited_JHP_CTJ']==288 and not receipt['full_chiral_sources_probes_trace_QAP_measure_phase_or_E5_A5']
out={'schema':'SBJ1_BOUNDARY_FLOW_REVIEW','elapsed_after_imports':time.perf_counter()-tick,'actual_heat_leg_derivative_recovers_old_bubble_flow_with_c2t':True,'boundary_subtraction_flow_sign_and_uniform_bound_checked':True,'beta_fin_and_nonlocal_log_slope_retained':True,'controls':controls,'minimum_fixed_face_subtraction_difference':mp.nstr(minfaces,30),'single_endpoint_countermodel_not_physical_admissibility_claim':True,'new_chiral_source_QAP_scheme_or_authority_promotion':False};print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
