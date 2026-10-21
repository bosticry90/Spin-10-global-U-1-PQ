"""Versioned preparation retaining the failed V1 input-adapter execution."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='14f963be9ae8968cdf6704aaa89b104a616f69fc'
old=json.loads((HERE/'preparation.json').read_bytes());deps=dict(old['input_sha256'])
for n,h in deps.items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
for name in ['prepare_v2.py','run_v2.py','primitive_v2.py','verify_v2.py','FAILURE_V1.md','CONTINUATION_V2.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(b)
    for f in [p,HERE/(name+'.source.txt')]:deps[str(f)]=sha256(f.read_bytes()).hexdigest()
for name in ['preparation.json','primary_capture.json']:
    p=HERE/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
value={**old,'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_PREPARATION_V2','input_sha256':dict(sorted(deps.items())),
       'V1_failure_preserved':True,'physical_inputs_methods_tolerances_limits_unchanged':True}
with (HERE/'preparation_v2.json').open('xb') as out:out.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('V2_FROZEN',len(deps),'bindings; V1 failed before color/amplitude')
