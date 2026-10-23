"""SRG1 corrected separate validation, preserving both original failures."""
from pathlib import Path
from hashlib import sha256
import json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/stationary-rg-pullback-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
for n in ['validation_v3_capture.json','validation_receipt_v3.json','controller_failure_v3.json']:assert not (HERE/n).exists(),n
assert not (CONTROL/'validation_v3_full_capture.json').exists()
for p,h in json.loads((HERE/'validation_preparation_v3.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
try:
    cap=capture([sys.executable,'-B',str(HERE/'verify_v3.py')]);dump(HERE/'validation_v3_capture.json',cap);dump(CONTROL/'validation_v3_full_capture.json',cap)
    if cap['exit_code']!=0:print(cap['stdout_and_stderr'],flush=True)
    assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
    assert cap['launch']['memory']['available_pagefile']>=350*1024**2 and cap['all_resource_samples']
    assert all('private_bytes' in x and x['private_bytes']<=8*1024**3 for x in cap['all_resource_samples'])
    result=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')]
    assert len(result)==1 and result[0]['elapsed_after_imports']<600
    assert result[0]['status'] in ['QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_AND_SCOPED_SCALE_IDENTITY','QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_WITH_FINITE_SCALE_MISMATCH']
    dump(HERE/'validation_receipt_v3.json',result[0])
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
    print('VALIDATION_V3_COMPLETED',result[0]['status'],result[0]['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure_v3.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
