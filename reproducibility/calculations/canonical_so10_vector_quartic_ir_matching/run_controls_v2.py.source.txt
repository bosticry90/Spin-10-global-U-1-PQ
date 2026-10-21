"""Run only the newly frozen explicit-mutant supplement, no native rerun."""
from pathlib import Path
from hashlib import sha256
import json,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-quartic-ir-matching-v1-2026-10-20')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,x):
    with p.open('xb') as out:out.write((json.dumps(x,sort_keys=True,indent=2)+'\n').encode())
for name in ['validation_preparation_v2.json','validation_preparation.json']:
    for n,h in json.loads((HERE/name).read_bytes())['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
c=capture([sys.executable,'-B',str(HERE/'verify_controls_v2.py')])
dump(HERE/'controls_v2_capture.json',c);dump(CONTROL/'controls_v2_full_capture.json',c)
if c['execution_state']!='COMPLETED':print(c['stdout_and_stderr'],flush=True)
assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed']
assert c['post_run_observations_qualified'] and c['private_allocation_limit_bytes']==8*1024**3
assert c['launch']['memory']['available_pagefile']>=350*1024**2
assert c['all_resource_samples'] and all(0<x['private_bytes']<=8*1024**3 for x in c['all_resource_samples'])
rows=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rows)==1
value=rows[0];assert value['elapsed_after_imports']<120
dump(HERE/'controls_v2_result.json',value)
old=json.loads((HERE/'validation_receipt.json').read_bytes());assert old['execution_state']=='COMPLETED'
receipt={**old,'schema':'C1_VECTOR_QUARTIC_IR_MATCHING_VALIDATION_V2',
 'completed_V1_natives_and_validation_reused_not_rerun':True,
 'V1_receipt_sha256':sha256((HERE/'validation_receipt.json').read_bytes()).hexdigest(),
 'explicit_mutant_supplement':value}
dump(HERE/'validation_receipt_v2.json',receipt)
print('V2_CONTROL_SUPPLEMENT_VALIDATED',value['elapsed_after_imports'],'completedV1reused',flush=True)
