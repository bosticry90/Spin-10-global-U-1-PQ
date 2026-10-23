"""Freeze V2 after authenticating the exact failed V1 execution."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='e94b6f59fbf7f933f273a46b6a1364f348005029'
old=json.loads((HERE/'preparation.json').read_bytes())
for n,h in old['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
cap=json.loads((HERE/'primary_capture.json').read_bytes())
assert cap['execution_state']=='FAILED' and cap['exit_code']==1 and cap['post_run_observations_qualified']
assert 'primary.py", line 49' in cap['stdout_and_stderr'] and 'AssertionError' in cap['stdout_and_stderr']
assert not (HERE/'primary_result.json').exists() and not (HERE/'primary_tables.json.gz').exists()
for name in ['primary_v2.py','run_v2.py','prepare_v2.py','FAILURE_V1.md']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(raw)
deps=dict(old['input_sha256'])
for p in HERE.iterdir():
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
new=dict(old);new.update({'schema':'MTA1_EXECUTION_PREPARATION_V2','input_sha256':deps,
    'preserved_failure':'primary_capture.json;controller_failure.json;original sources',
    'only_mathematical_correction':'COMPARE_UNROUNDED_METRIC_ROUNDTRIP_AT_UNCHANGED_1e-70',
    'scientific_inputs_or_requirements_changed':False})
with (HERE/'execution_preparation_v2.json').open('xb') as out:out.write((json.dumps(new,sort_keys=True,indent=2)+'\n').encode())
print('MTA1_V2_FROZEN',len(deps),'bindings; failed V1 not relabelled',flush=True)
