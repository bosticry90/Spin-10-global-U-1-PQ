"""GVA1 append-only source/evidence freeze for subsequent bounded phases."""
from pathlib import Path
from hashlib import sha256
import json,ast,sys,re
HERE=Path(__file__).resolve().parent
phase=sys.argv[1];assert re.fullmatch('[a-z0-9_]+',phase)
deps=json.loads((HERE/'preparation.json').read_bytes())['input_sha256']
for p,h in deps.items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for p in sorted(HERE.iterdir()):
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in sys.argv[2:]:
    p=HERE/n;assert p.parent==HERE;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt')
    if cp.exists():assert cp.read_bytes()==raw
    else:
        with cp.open('xb') as f:f.write(raw)
    deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
with (HERE/(phase+'_preparation.json')).open('xb') as f:f.write((json.dumps({'schema':'GVA1_PHASE_PREPARATION','phase':phase,
 'input_sha256':dict(sorted(deps.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,
 'whole_package_cap':6*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('FROZEN_PHASE',phase,len(deps),'bindings',flush=True)
