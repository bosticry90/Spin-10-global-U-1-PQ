"""SRM1 V3 freeze corrected verifier and authenticate completed V2 natives."""
from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='4c2de406c8993d954d6a05dcd61d5191bf857abe'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/source-region-matching-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==BASE
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
bindings={};cache={}
for name in ['preparation.json','preparation_v2.json','validation_preparation_v2.json']:
    for p,h in json.loads((HERE/name).read_bytes())['input_sha256'].items():
        if p not in cache:cache[p]=sha256(Path(p).read_bytes()).hexdigest()
        assert cache[p]==h,p;bindings[p]=h
for role in ['primary_v2','replay_v2']:
    c=json.loads((HERE/(role+'_capture.json')).read_bytes());r=json.loads((HERE/(role+'_result.json')).read_bytes())
    assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
    blob=(HERE/(role+'_tables.json.gz')).read_bytes()
    assert sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
    assert (HERE/(role+'_capture.json')).read_bytes()==(CONTROL/(role+'_full_capture.json')).read_bytes()
c=json.loads((HERE/'validation_v2_capture.json').read_bytes());assert c['execution_state']=='FAILED' and c['exit_code']==1
assert "AttributeError: 'Zero' object has no attribute 'bit_count'" in c['stdout_and_stderr']
assert not (HERE/'validation_receipt_v2.json').exists()
for name in ['FAILURE_V2.md','CONTINUATION_V3.md','verify_v3.py','prepare_v3.py','run_v3.py']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
for p in HERE.iterdir():
    if p.is_file():bindings[str(p)]=sha256(p.read_bytes()).hexdigest()
with (HERE/'validation_preparation_v3.json').open('xb') as f:f.write((json.dumps({'schema':'SRM1_V3_VALIDATION_PREPARATION','base_commit':BASE,
    'input_sha256':dict(sorted(bindings.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,
    'completed_natives_reused':['primary_v2','replay_v2'],'failed_original_executions_preserved':2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('V3_VALIDATION_FROZEN',len(bindings),'bindings;no native rerun',flush=True)
