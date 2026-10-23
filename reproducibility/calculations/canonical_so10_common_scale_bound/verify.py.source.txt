"""CSB1 certify the rational data bounds and classify common-L feasibility."""
from data import *
from replay import solve,interval
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();mp.mp.dps=100
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz');old=packed(CAL/'canonical_so10_bosonic_interior_assembly/primary_tables.json.gz')
maximum=mp.mpf(0);compared=0;certified=0;permutations=0;omission_insensitive=0
def compare(a,b):
 global maximum,compared
 aa,bb=q(a),q(b);er=abs(aa-bb)/(1+abs(aa));maximum=max(maximum,er);assert er<mp.mpf('1e-28');compared+=1
assert set(A['cases'])==set(B['cases'])=={'1/2','3/4','1'}
for d in [A,B]:assert d['tau_lo']==str(TAU_LO) and d['tau_hi']==str(TAU_HI) and not d['physical_scale_adopted'] and not d['RG_trajectory_or_full_theory_exclusion']
for key,a in A['cases'].items():
 b=B['cases'][key]
 for name in ['A','B','L0_normalized']:
  for v,z in zip(a[name],b[name]):compare(v,z)
 for name in ['minimum_unscaled','witness_L','normalized_minimum','coarse_normalized_lower','coarse_normalized_upper']:
  compare(a[name],b[name])
 for v,z in zip(a['loose_tree_interval'],b['loose_tree_interval']):compare(v,z)
 assert a['feasible_loose_tree']==b['feasible_loose_tree']
 AA,BB=list(map(F,a['A'])),list(map(F,a['B']));T,L=F(a['minimum_unscaled']),F(a['witness_L'])
 assert max(abs(x+y*L) for x,y in zip(AA,BB))==T
 assert list(map(F,a['residuals_unscaled']))==[x+y*L for x,y in zip(AA,BB)]
 for row in a['pair_bounds']:
  i,j=row['pair'];bound=abs(BB[j]*AA[i]-BB[i]*AA[j])/(BB[i]+BB[j]);assert bound==F(row['bound']) and bound<=T
 assert max(F(row['bound']) for row in a['pair_bounds'])==T
 assert F(a['coarse_normalized_lower'])==T/TAU_HI and F(a['coarse_normalized_upper'])==T/TAU_LO
 assert q(a['coarse_normalized_lower'])<=q(a['normalized_minimum'])<=q(a['coarse_normalized_upper'])
 lo,hi=interval(AA,BB,TAU_HI);assert [lo,hi]==list(map(F,a['loose_tree_interval'])) and (lo<=hi)==a['feasible_loose_tree']
 impossible=not a['feasible_loose_tree'];assert impossible==(T>TAU_HI);certified+=int(impossible)
 assert all(F(v)==0 for v in a['separate_scales_residuals'])
 for v in a['omitted_constraint_minima']:
  assert F(v)<=T;omission_insensitive+=int(F(v)==T)
 pp=[2,0,1];tp,lp,_,_=solve([AA[i] for i in pp],[BB[i] for i in pp]);assert tp==T and max(abs(x+y*lp) for x,y in zip(AA,BB))==T;permutations+=1
 for v,row in zip(a['L0_normalized'],old['cases'][key]['kinetic']):compare(v,row['k2'])
print('RESULT '+json.dumps({'status':'QUALIFIED_FROZEN_BOSONIC_COMMON_SCALE_MINIMAX_BOUND','elapsed_after_imports':time.perf_counter()-start,'coupling_cases':3,'route_and_L0_comparisons':compared,'permutation_checks':permutations,'maximum_scaled_error':mp.nstr(maximum,35),'certified_infeasible_common_logs_at_loose_tree_threshold':certified,'insensitive_omission_controls':omission_insensitive,'exact_algebra_on_frozen_decimal_tables':True,'physical_RG_or_full_theory_exclusion':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
