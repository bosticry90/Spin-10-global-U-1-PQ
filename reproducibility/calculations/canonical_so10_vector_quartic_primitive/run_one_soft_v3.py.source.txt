"""Execute only the newly frozen open-kernel/IR supplement, reuse V2."""
from pathlib import Path
from hashlib import sha256
import json,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-quartic-primitive-v1-2026-10-20')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
prep=json.loads((HERE/'validation_preparation_v3.json').read_bytes())
for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
nested=json.loads((HERE/'validation_preparation_v2.json').read_bytes())
for n,h in nested['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
cap=capture([sys.executable,'-B',str(HERE/'verify_one_soft_v3.py')])
dump(HERE/'supplement_v3_capture.json',cap);dump(CONTROL/'supplement_v3_full_capture.json',cap)
if cap['execution_state']!='COMPLETED':print(cap['stdout_and_stderr'],flush=True)
assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and cap['calculation_completed']
assert cap['post_run_observations_qualified'] and cap['private_allocation_limit_bytes']==8*1024**3
assert cap['launch']['memory']['available_pagefile']>=350*1024**2
assert cap['all_resource_samples'] and all(0<x['private_bytes']<=8*1024**3 for x in cap['all_resource_samples'])
rows=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rows)==1
supp=rows[0];assert supp['elapsed_after_imports']<120
dump(HERE/'one_soft_supplement_v3.json',supp)
prior=json.loads((HERE/'validation_receipt_v2.json').read_bytes())
assert prior['execution_state']=='COMPLETED' and sha256((HERE/'validation_receipt_v2.json').read_bytes()).hexdigest()=='a7495823ebe1d8a96388d7bb51c8c50e005f37c04c200332426e30ee925f8398'
value={**prior,'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_VALIDATION_V3',
 'status':'QUALIFIED_COMPLETE_REGULATED_BARE_QUARTIC_AND_ACTUAL_ONE_SOFT_INVERSE_IR_CLOSURE',
 'V2_receipt_sha256':sha256((HERE/'validation_receipt_v2.json').read_bytes()).hexdigest(),
 'completed_V2_natives_and_validation_reused_not_rerun':True,
 'V1_schema_failure_and_watchdog_delay_preserved':True,'actual_one_soft_supplement':supp}
dump(HERE/'validation_receipt_v3.json',value)
print('V3_SUPPLEMENT_VALIDATED',supp['elapsed_after_imports'],'V2 notrerun',flush=True)
