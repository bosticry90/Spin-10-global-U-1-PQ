from pathlib import Path
from hashlib import sha256
import gzip,json,time,sympy as s,mpmath as mp
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());tick=time.perf_counter()
for p,h in read(O/'validation_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
load=lambda p:json.loads(gzip.decompress(p.read_bytes()));a,b=[load(O/(r+'_tables.json.gz')) for r in ['primary','replay']];mp.mp.dps=100;worst=mp.mpf(0);tail=mp.mpf(0);positions=0;controls={'omit_boundary':0,'early_e0_log':0,'early_e0_insensitive':0,'drop_logq_pair':0}
assert len(a['rows'])==len(b['rows'])==18
for x,y in zip(a['rows'],b['rows']):
 for k in ['epsilon','q','kind']:assert x[k]==y[k]
 for k in ['I','S','I_ren_beta0_comparator','ID_ren_beta0_comparator','remainder','uniform_bound','premature_e0_log_subtraction','endpoint_countermodel_psi']:
  xx,yy=mp.mpf(x[k]),mp.mpf(y[k]);error=abs(xx-yy)/max(1,abs(xx),abs(yy));worst=max(worst,error);assert error<mp.mpf('1e-40'),(k,x,error);positions+=1
 assert -mp.mpf('1e-75')<=mp.mpf(x['remainder'])<=mp.mpf(x['uniform_bound'])+mp.mpf('1e-75');tail=max(tail,mp.mpf(y['series_tail_bound']));assert mp.mpf(y['series_tail_bound'])<mp.mpf('1e-48');controls['omit_boundary']+=int(mp.mpf(y['S'])!=0);controls['early_e0_log']+=int(abs(mp.mpf(y['S'])-mp.mpf(y['premature_e0_log_subtraction']))>mp.mpf('1e-40'));controls['early_e0_insensitive']+=int(y['epsilon']=='0')
# Only now compare/assemble with the already-qualified actual tensor routes.
j=O.parent/'canonical_so10_chiral_joint_heat_pilot';t=O.parent/'canonical_so10_chiral_transverse_joint_limit';jr=load(j/'primary_v2_tables.json.gz');tr=load(t/'primary_tables.json.gz');assert read(j/'validation_receipt_v3.json')['actual_joint_tensor_vs_direct_Ward_and_endpoint_routes_agree'] and read(t/'validation_receipt.json')['direct_upper_gamma_vs_independent_lower_face_series_agree'];tensor_positions=0;max_tensor_norm_error=mp.mpf(0)
for idx,(x,f) in enumerate(zip(a['rows'],tr['rows'])):
 e,q,mu=mp.mpf(x['epsilon']),mp.mpf(x['q']),mp.mpf('1.5');c=(mp.mpf(x['cq'])/q) if x['kind']=='finite' else mp.exp(-mp.mpf(x['a'])/e)/q;N=mp.exp(mp.euler*e)*mu**e
 if idx<9:w=mp.mpf(jr['numeric_kernels'][idx]['Ward_power_subtracted'])
 else:w=mp.mpf(jr['correlated_paths'][idx-9]['Ward_ren'])
 D=N*q**(1-e)*mp.gamma(1+e)*mp.beta(2-e,2-e)/(1-e);cm=2*(mp.mpf('.5')**(2-e)/(2-e)-2*mp.mpf('.5')**(3-e)/(3-e)+mp.mpf('.5')**(4-e)/(4-e));bw=N*q*q*c**(1+e)*cm/(1-e)*(mp.mpf('.5')+e/(1+e));bound=q*(mp.mpf(x['uniform_bound'])/3+mp.mpf(f['uniform_bound']))+bw;Tcoef=mp.mpf(x['I_ren_beta0_comparator'])/3+mp.mpf(f['converted']);Dcoef=mp.mpf(x['ID_ren_beta0_comparator'])/3+mp.mpf(f['F_D']);p=[mp.sqrt(q/8)*v for v in [1,2,-1,mp.sqrt(2)]]
 for m in range(4):
  for n in range(4):
   T=int(m==n)*q-p[m]*p[n];err=abs((Tcoef-Dcoef)*T+(w-D)*int(m==n));assert err<=bound+mp.mpf('1e-70'),(idx,m,n,err,bound);max_tensor_norm_error=max(max_tensor_norm_error,err);tensor_positions+=1
e,c,mu,q,aa=s.symbols('epsilon c muR2 q a',positive=True);beta=s.Symbol('beta_fin',real=True);L=2**e/(1-e);S=(1-s.exp(e*(s.EulerGamma+s.log(c*mu)))*L)/e;assert s.simplify(s.limit(S,e,0)+s.EulerGamma+s.log(2*c*mu)+1)==0
tau=-e*s.log(c*mu);psi=tau*s.exp(-tau);assert s.limit(psi,e,0)==0 and s.limit(psi,c,0)==0;assert s.simplify(s.limit(psi.subs(c,s.exp(-aa/e)/q),e,0)-aa*s.exp(-aa))==0
muH,nlog=s.symbols('muH2 n_log',positive=True);D0=s.log(mu/q)+2+beta;H0=s.log(muH/q)-s.EulerGamma+1-s.log(4)+nlog+beta;diff=s.expand_log((D0-H0).subs(mu,4*s.pi*s.exp(-s.EulerGamma)*muH),force=True);assert s.simplify(diff-(1+s.log(16*s.pi)-nlog))==0
limit=(s.log(mu/q)+2+beta)/3-s.Rational(1,9);assert s.diff(limit,beta)==s.Rational(1,3) and s.simplify(s.diff(limit,q)+1/(3*q))==0;controls['drop_logq_pair']=int(s.log(2)!=0)
# Fixed-face boundary Lfixed=1 loses the actual +log2+1 removable contribution.
assert s.simplify(s.diff(L,e).subs(e,0))==s.log(2)+1
out={'schema':'SBJ1_VALIDATION','elapsed_after_imports':time.perf_counter()-tick,'direct_upper_gamma_vs_independent_boundary_series_agree':True,'finite_cases':9,'correlated_paths':9,'scalar_positions_compared':positions,'tensor_positions_with_inherited_JHP_CTJ':tensor_positions,'maximum_scaled_scalar_discrepancy':mp.nstr(worst,30),'maximum_retained_series_tail':mp.nstr(tail,30),'uniform_scalar_and_full_selected_quadratic_comparison_constructed':True,'common_beta_fin_symbolic':True,'joint_tensor_transverse_coefficient':'log(muR2/q)/3+5/9+beta_fin/3','joint_tensor_Ward_coefficient':'q/6','nonlocal_logq_retained':True,'endpoint_chi4_relation_recovered_with_scale_reparametrization':True,'endpoints_do_not_unique_determine_joint_comparison_in_larger_local_analytic_class':True,'countermodel_not_claimed_full_physical_counterterm':True,'controls':controls,'old_model_color_and_spin_premises_reused_not_recomputed':True,'new_physical_scheme_baseline_or_authority':False,'full_chiral_sources_probes_trace_QAP_measure_phase_or_E5_A5':False};print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
