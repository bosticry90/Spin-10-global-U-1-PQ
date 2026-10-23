"""SRM1 V2 preserve exact failure and freeze the serialization-only continuation."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='4c2de406c8993d954d6a05dcd61d5191bf857abe'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/source-region-matching-v1-2026-10-21')
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bindings={}
for p,h in json.loads((HERE/'preparation.json').read_bytes())['input_sha256'].items():
    assert sha256(Path(p).read_bytes()).hexdigest()==h,p;bindings[p]=h
cap=json.loads((HERE/'primary_capture.json').read_bytes())
assert cap['execution_state']=='FAILED' and cap['exit_code']==1
assert 'TypeError: Object of type One is not JSON serializable' in cap['stdout_and_stderr']
assert (HERE/'primary_capture.json').read_bytes()==(CONTROL/'primary_full_capture.json').read_bytes()
assert not (HERE/'primary_tables.json.gz').exists() and not (HERE/'validation_receipt.json').exists()
for role in ['primary','replay']:
    old=(HERE/(role+'.py')).read_text();new=(HERE/(role+'_v2.py')).read_text()
    assert new.replace('from data_v2 import *','from data import *')==old
expected=(HERE/'verify.py').read_text().replace("HERE/'validation_preparation.json'","HERE/'validation_preparation_v2.json'").replace("HERE/'primary_tables.json.gz'","HERE/'primary_v2_tables.json.gz'").replace("HERE/'replay_tables.json.gz'","HERE/'replay_v2_tables.json.gz'")
assert (HERE/'verify_v2.py').read_text()==expected
for name in ['FAILURE_V1.md','CONTINUATION_V2.md','data_v2.py','primary_v2.py','replay_v2.py','verify_v2.py','prepare_v2.py','run_v2.py']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
for p in HERE.iterdir():
    if p.is_file():bindings[str(p)]=sha256(p.read_bytes()).hexdigest()
assert len((CONTROL/'old_git_tree.txt').read_bytes().splitlines())==28861
with (HERE/'preparation_v2.json').open('xb') as f:f.write((json.dumps({'schema':'SRM1_V2_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bindings.items())),
    'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,
    'V1_execution':'FAILED_SERIALIZATION_NO_TABLE','science_unchanged':True,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('V2_FROZEN',len(bindings),'bindings;V1 failure preserved',flush=True)
