"""HPR1 recover a completed frozen result after outer status-label mismatch."""
from pathlib import Path
from hashlib import sha256
import json,time
H=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/hard-pole-remainder-v1-2026-10-21')
start=time.perf_counter()
prep=json.loads((H/'recovery_preparation_v2.json').read_bytes())
for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
f=json.loads((H/'controller_failure.json').read_bytes())
assert f['execution_state']=='FAILED' and not f['failed_controller_counted_as_PASS']
assert sha256((H/'run_supplement.py').read_bytes()).hexdigest()==f['failed_controller_sha256']
assert sha256((H/'adversarial_capture.json').read_bytes()).hexdigest()==f['completed_native_capture_sha256']
c=json.loads((H/'adversarial_capture.json').read_bytes())
assert (H/'adversarial_capture.json').read_bytes()==(C/'adversarial_full_capture.json').read_bytes()
assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['post_run_observations_qualified'] and c['calculation_completed']
assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples']
assert max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
out=[json.loads(z[7:]) for z in c['stdout_and_stderr'].splitlines() if z.startswith('RESULT ')]
assert len(out)==1 and out[0]['status']=='QUALIFIED_HPR1_EXPLICIT_POLE_AND_FINITE_MUTATIONS'
assert out[0]['elapsed_after_imports']<600 and out[0]['scientific_acceptance']=='NOT_PERFORMED'
assert out[0]['main_receipt_sha256']==sha256((H/'validation_receipt.json').read_bytes()).hexdigest()
with (H/'adversarial_receipt.json').open('xb') as file:file.write((json.dumps(out[0],sort_keys=True,separators=(',',':'))+'\n').encode())
r={'schema':'HPR1_METADATA_RECOVERY','execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','scientific_calculations_rerun':0,'old_completed_RESULT_preserved_exactly':True,'failed_controller_preserved':True,'native_capture_sha256':sha256((H/'adversarial_capture.json').read_bytes()).hexdigest(),'controller_failure_sha256':sha256((H/'controller_failure.json').read_bytes()).hexdigest(),'adversarial_receipt_sha256':sha256((H/'adversarial_receipt.json').read_bytes()).hexdigest(),'elapsed_seconds':time.perf_counter()-start}
for p in [H/'recovery_receipt_v2.json',C/'metadata_recovery_v2.json']:
 with p.open('xb') as file:file.write((json.dumps(r,sort_keys=True,indent=2)+'\n').encode())
print(json.dumps(r,sort_keys=True),flush=True)
