from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/joint-marginal-fermion-normalization-v1-2026-10-23')
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
old=read(HERE/'preparation.json');bind=dict(old['input_sha256'])
for p,h in bind.items():assert digest(Path(p))==h,p
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==old['base_commit']
assert read(HERE/'primary_capture.json')['exit_code']==0 and read(HERE/'replay_capture.json')['exit_code']==1
assert read(HERE/'controller_failure.json')['last_role']=='replay'
assert not (HERE/'replay_tables.json.gz').exists() and not (HERE/'validation_receipt.json').exists()
for p in HERE.iterdir():
 if p.is_file():bind[str(p)]=digest(p)
for n in ['CONTINUATION_V2.md','replay_v2.py','prepare_v2.py','run_v2.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 bind[str(HERE/(n+'.source.txt'))]=digest(HERE/(n+'.source.txt'))
with (HERE/'preparation_v2.json').open('xb') as f:f.write((json.dumps({'schema':'JMF1_PREPARATION_V2','input_sha256':bind,'completed_primary_reused':True,'same_acceptance_and_resource_limits':True,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('JMF1_V2_FROZEN',len(bind),'bindings',flush=True)
