"""BLH1 authenticate arithmetic and classify the actual hierarchy outcome."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();mp.mp.dps=95
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz');assert len(A['rows'])==len(B['rows'])==6
maximum=mp.mpf(0);positions=0;outcomes=[]
for a,b in zip(A['rows'],B['rows']):
 assert (a['x'],a['gauge'])==(b['x'],b['gauge']) and a['necessary_hierarchy']==b['necessary_hierarchy']
 for key in ['lambda1','lambda2','k1','k2','K_truncated','inverse_alpha_tree','inverse_alpha_shift1','inverse_alpha_shift2','two_vs_tree','two_vs_one']:
  er=abs(q(a[key])-q(b[key]))/(1+abs(q(a[key])));maximum=max(maximum,er);assert er<mp.mpf('1e-35');positions+=1
 actual=abs(q(a['k2']))<1 and abs(q(a['k2']))<abs(q(a['k1']));assert actual==a['necessary_hierarchy'];outcomes.append(actual)
 assert abs(q(a['missing_loop_factor_control']))>mp.mpf('1e-20')
 if a['x']=='1/2':assert abs(q(a['missing_external_x_control']))>mp.mpf('1e-20')
 else:assert q(a['missing_external_x_control'])==0
print('RESULT '+json.dumps({'status':'QUALIFIED_BOSONIC_LOOP_HIERARCHY_DIAGNOSTIC','elapsed_after_imports':time.perf_counter()-start,'numeric_positions':positions,'gauge_coupling_positions':6,'maximum_scaled_error':mp.nstr(maximum,35),'necessary_hierarchy_passes':sum(outcomes),'necessary_hierarchy_failures':len(outcomes)-sum(outcomes),'scope':'TWO_FIXED_DIAGNOSTICS_NOT_ALL_COUPLINGS_OR_FULL_MATTER','scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
