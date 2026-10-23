"""SRM1 V3 observed verifier only;no native recomputation or failure deletion."""
from pathlib import Path
from hashlib import sha256
import json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/source-region-matching-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
for p,h in json.loads((HERE/'validation_preparation_v3.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for name in ['validation_v3_capture.json','validation_receipt_v3.json','controller_failure_v3.json']:assert not (HERE/name).exists()
assert not (CONTROL/'validation_v3_full_capture.json').exists()
try:
    c=capture([sys.executable,'-B',str(HERE/'verify_v3.py')]);dump(HERE/'validation_v3_capture.json',c);dump(CONTROL/'validation_v3_full_capture.json',c)
    if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
    assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
    assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples']
    assert all(v['private_bytes']<=8*1024**3 for v in c['all_resource_samples'])
    rows=[json.loads(line[7:]) for line in c['stdout_and_stderr'].splitlines() if line.startswith('RESULT ')]
    assert len(rows)==1;r=rows[0]
    assert r['status']=='QUALIFIED_FORMAL_SOURCE_REGION_MATCHING_AND_LOCAL_BOSONIC_WIDTH_IDENTITY' and r['elapsed_after_imports']<600
    dump(HERE/'validation_receipt_v3.json',r)
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
    print('V3_VERIFIER_COMPLETED',r['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure_v3.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
