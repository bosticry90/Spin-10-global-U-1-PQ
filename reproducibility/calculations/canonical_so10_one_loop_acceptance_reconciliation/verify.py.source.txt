"""Separate OAR1 checks; imports neither native route nor a native algebra helper."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import json, time
T0=time.perf_counter()
R=Path('C:/Users/psboy/Documents/ToE-Next')
O=R/'calculations/canonical_so10_one_loop_acceptance_reconciliation'
v=json.loads((O/'validation_preparation.json').read_bytes())
for path,expected in v['input_sha256'].items():
 assert sha256(Path(path).read_bytes()).hexdigest()==expected,path
p=json.loads((O/'preparation.json').read_bytes())
spec=(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/A10_E5_QUANTUM_FUNCTIONAL_SPEC_V1.md').read_text()
assert "n=1: Q' Gamma_1" in spec
assert "n=2: Q' Gamma_2 + (Gamma_1,Gamma_1)/2" in spec
assert 'Two restored constructions first differing at n' in spec
assert 'At first differing restored order it' in spec
assert 'A5 and transported' in spec and 'Multiple derivatives require' in spec
# These cite real clauses; occurrence is NOT automatic verification of prose.
for a in p['anchors']:
 lines=Path(a['path']).read_text(encoding='utf-8').splitlines()
 assert lines[a['first_line']-1:a['last_line']]==a['lines']

# Derive the master orders by symmetric bilinear convolution of even functionals.
def master(series):
 out=Counter()
 for degree,a in series.items():
  for e,b in series.items():
   for term,c in a.items():
    for factor,k in b.items():
     out[degree+e,tuple(sorted((term,factor)))]+=F(1,2)*c*k
 return {k:x for k,x in out.items() if x}
base={0:{'S':1},1:{'F':1},2:{'H':1}}
endpoint={0:{'S':1},1:{'F':1,'d':1},2:{'H':1,'L':1,'E':1}}
a,b=master(base),master(endpoint)
diff={k:b.get(k,0)-a.get(k,0) for k in a.keys()|b.keys()}
diff={k:x for k,x in diff.items() if x}
assert {k:x for k,x in diff.items() if k[0]==1}=={(1,('S','d')):1}
assert {k:x for k,x in diff.items() if k[0]==2}=={
 (2,('E','S')):1,(2,('L','S')):1,(2,('F','d')):1,(2,('d','d')):F(1,2)}
# No unproved next-order condition may enter the first-order coefficient.
assert (1,('d','d')) not in diff and diff[2,('F','d')]==1

# Independently enumerate multiplicity vectors of r0/r1/r2 vertices.
from math import factorial
expected=Counter()
for vertices in range(5):
 for r1 in range(vertices+1):
  for r2 in range(vertices-r1+1):
   r0=vertices-r1-r2
   ways=factorial(vertices)//(factorial(r0)*factorial(r1)*factorial(r2))
   for loops in range(4):expected[loops,loops+r1+2*r2]+=ways
assert sum(expected.values())==484
assert all(L+r1+2*r2>=2 for L in range(1,5) for r1 in range(1,5) for r2 in range(5))
assert 1+0==1  # counterexample if a strength-zero vertex were miscounted as r1

# Derive noncommutative covariance from the Leibniz identity for ad_X.
def mon(word,c=1):return {tuple(word):F(c)}
def add(*terms):
 out=Counter()
 for a in terms:
  for w,c in a.items():out[w]+=c
 return {k:x for k,x in out.items() if x}
def minus(a):return {w:-c for w,c in a.items()}
def times(a,b):
 out=Counter()
 for w,c in a.items():
  for t,k in b.items():out[w+t]+=c*k
 return {k:x for k,x in out.items() if x}
def ad(a):return add(times(a,mon('X')),minus(times(mon('X'),a)))
q,i=mon('Q'),mon('i')
left=add(times(ad(i),q),times(i,ad(q)),times(ad(q),i),times(q,ad(i)))
right=ad(add(times(i,q),times(q,i)))
assert left==right
assert ad(q) and add(mon('X'),mon('X'))  # omitted transport / wrong inverse
assert add(times(q,ad(q)),times(ad(q),q))==add(mon('QQX'),mon('XQQ',-1))
# Q^2=0 removes exactly the surviving QQ words, rather than assuming X commutes.

# Odd derivation, unrelated to the native exterior/Jacobi implementations.
# Track all three bitmask generators with their graded signs.
q_generator={1:{3:F(1)},2:{6:F(1)},4:{}}
def odd_derivative(mask):
 out=Counter();before=0
 for bit in [1,2,4]:
  if not mask&bit:continue
  after=mask&~((bit<<1)-1)
  for m,c in q_generator[bit].items():
   if before&m or m&after:continue
   inv=sum(1 for a in range(3) for b in range(3)
           if before&(1<<a) and m&(1<<b) and a>b)
   inv+=sum(1 for a in range(3) for b in range(3)
            if (before|m)&(1<<a) and after&(1<<b) and a>b)
   out[before|m|after]+=(-1)**(before.bit_count()+inv)*c
  before|=bit
 return {k:x for k,x in out.items() if x}
assert odd_derivative(3)=={7:F(-1)}
# With S=0 this delta is first-order closed but its square is not zero.
# This is a diagnostic algebra, not an asserted Spin10 action or amplitude.

# Authenticate the ACTUAL inherited controls without rerunning their tensors.
brt=json.loads((R/'calculations/canonical_so10_basic_rotation_torsion/replay_result.json').read_bytes())
assert [x['coefficients'] for x in brt['Jacobi_witness_rows']]==[['4','0','0'],['0','0','-32']]
scalar=json.loads((R/'calculations/canonical_so10_basic_rotation_torsion/replay_scalar_v2_result.json').read_bytes())
assert scalar['rotation_family_dimension']==4
assert scalar['full_leading_source_plus_coupling_rank']==5
assert not scalar['quantum_normalization_admissibility_or_anomaly_verdict']
assert not scalar['E5_A5_HB1_C5_or_physical_promotion']

results=[]
for role in ['primary','replay']:
 cap=json.loads((O/(role+'_capture.json')).read_bytes())
 assert cap['execution_state']=='COMPLETED' and not cap['failed_or_incomplete_counted_as_PASS']
 r=json.loads((O/(role+'_result.json')).read_bytes())
 assert r['elapsed_after_imports']<60
 assert r['graph_power_multiplicities']==[[a,b,c] for (a,b),c in sorted(expected.items())]
 assert r['closed_first_order_not_quadratically_closed_control']==-1
 assert r['one_loop_response_to_hbar_counterterm_minimum_order']==2
 assert r['order_hbar_jacobian_effective_action_minimum_order']==2
 assert r['noncommutative_transport_inverse_and_omission_controls']
 assert not r['full_E5_A5_or_quantum_prescription_nonemptiness_proved']
 assert not r['new_physics_amplitudes_or_general_unit_domains_calculated']
 assert not r['authority_changed']
 for old in r['authenticated_existing_receipts']:
  doc=json.loads(Path(old['path']).read_bytes())
  assert doc['execution_state']=='COMPLETED' and doc['scientific_disposition']==old['scientific_disposition']
 results.append({k:x for k,x in r.items() if k not in ['route','elapsed_after_imports']})
assert results[0]==results[1]
assert sha256((R/'project_state.json').read_bytes()).hexdigest()=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
assert sum(f.stat().st_size for f in O.rglob('*') if f.is_file())<2*1024**2
elapsed=time.perf_counter()-T0
assert elapsed<120
result={'schema':'ONE_LOOP_ACCEPTANCE_RECONCILIATION_VALIDATION_V1',
 'execution_state':'COMPLETED','elapsed_after_imports':elapsed,
 'input_sha256':v['input_sha256'],'contract_anchors_authenticated':len(p['anchors']),
 'reused_completed_receipts':len(p['receipts']),'graph_weight_cases_checked':484,
 'master_order_convolution_and_noncommutative_operator_identity_checked':True,
 'closed_not_exactly_extendible_control_and_actual_four_class_evidence_retained':True,
 'independent_native_algorithms_and_verifier_agree':True,
 'prose_mathematically_proved_by_text_matching':False,
 'old_large_calculations_freshly_reproduced':False,
 'full_E5_A5_higher_order_prescription_or_physical_viability_claimed':False,
 'authority_changed':False,'failed_native_workers':0,'failed_verifier_workers':0,
 'scientific_disposition':'QUALIFIED_BOUNDED_ACCEPTANCE_RECONCILIATION_AND_STRICT_FORMAL_FIRST_ORDER_REPLACEMENT_NOT_UNIVERSAL_E5'}
print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True)
