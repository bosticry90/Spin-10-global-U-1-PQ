"""Freeze the small actual one-soft identification after completed V2."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='14f963be9ae8968cdf6704aaa89b104a616f69fc'
old=HERE/'validation_preparation_v2.json'
for n,h in json.loads(old.read_bytes())['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
deps={str(old):sha256(old.read_bytes()).hexdigest()}
for name in ['prepare_one_soft_v3.py','run_one_soft_v3.py','verify_one_soft_v3.py','ONE_SOFT_SUPPLEMENT_V3.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(b)
    for f in [p,HERE/(name+'.source.txt')]:deps[str(f)]=sha256(f.read_bytes()).hexdigest()
for name in ['primary_v2_tables.json.gz','replay_v2_tables.json.gz','primary_v2_result.json',
             'replay_v2_result.json','validation_v2_capture.json','validation_receipt_v2.json','FAILURE_V1.md']:
    p=HERE/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
state=ROOT/'project_state.json';assert sha256(state.read_bytes()).hexdigest()=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
deps[str(state)]=sha256(state.read_bytes()).hexdigest()
value={'schema':'C1_VECTOR_QUARTIC_ONE_SOFT_PREPARATION_V3','input_sha256':deps,
       'nested_input_manifest':str(old),'completed_V2_reused_not_replayed':True,
       'supplement_seconds':120,'private_sampled_cap':8*1024**3,'launch_floor':350*1024**2,
       'whole_package_limit':2*1024**2,'scientific_acceptance':'NOT_PERFORMED'}
with (HERE/'validation_preparation_v3.json').open('xb') as out:out.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('ONE_SOFT_SUPPLEMENT_FROZEN',len(deps),'directbindings plus frozenV2 nestedmanifest')
