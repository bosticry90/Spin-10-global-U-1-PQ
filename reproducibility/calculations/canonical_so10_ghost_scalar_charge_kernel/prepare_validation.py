"""Freeze completed GSK1 native tables and a separate validator."""
from pathlib import Path
from hashlib import sha256
import json,ast
HERE=Path(__file__).resolve().parent
deps=json.loads((HERE/'preparation.json').read_bytes())['input_sha256']
for p,h in deps.items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for p in sorted(HERE.iterdir()):
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['verify.py','prepare_validation.py','run_validation.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw;ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt')
    with cp.open('xb') as f:f.write(raw)
    deps[str(cp)]=sha256(raw).hexdigest()
v={'schema':'GSK1_VALIDATION_PREPARATION','input_sha256':dict(sorted(deps.items())),
 'seconds':600,'scientific_acceptance':'NOT_PERFORMED'}
with (HERE/'validation_preparation.json').open('xb') as f:f.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN_VALIDATION',len(deps),'bindings',flush=True)
