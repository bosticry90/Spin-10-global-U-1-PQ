"""Freeze explicit mutant supplement while preserving completed V1."""
from pathlib import Path
from hashlib import sha256
import ast,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
old=HERE/'validation_preparation.json';deps={str(old):sha256(old.read_bytes()).hexdigest()}
for n,h in json.loads(old.read_bytes())['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
for name in ['prepare_controls_v2.py','run_controls_v2.py','verify_controls_v2.py','VALIDATION_SUPPLEMENT_V2.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(b)
    for f in [p,HERE/(name+'.source.txt')]:deps[str(f)]=sha256(f.read_bytes()).hexdigest()
for name in ['validation_receipt.json','validation_capture.json','primary_tables.json.gz','replay_tables.json.gz']:
    p=HERE/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
value={'schema':'C1_VECTOR_QUARTIC_IR_CONTROL_PREPARATION_V2','input_sha256':deps,
       'nested_input_manifest':str(old),'supplement_seconds':120,'sampled_private_cap':8*1024**3,
       'launch_floor':350*1024**2,'whole_package_bytes':2*1024**2,'scientific_acceptance':'NOT_PERFORMED'}
with (HERE/'validation_preparation_v2.json').open('xb') as out:out.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('CONTROL_SUPPLEMENT_FROZEN',len(deps),'directbindings plusnestedmanifest')
