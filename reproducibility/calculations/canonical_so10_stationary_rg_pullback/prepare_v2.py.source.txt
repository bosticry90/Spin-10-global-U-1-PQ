"""SRG1 V2 explicit parameter namespace and separate artifact freeze."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='45352e8d446f60000c1caaa1900e03317e1f78e4'
old=json.loads((HERE/'preparation.json').read_bytes())
for p,h in old['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
cap=json.loads((HERE/'primary_capture.json').read_bytes())
assert cap['exit_code']==1 and cap['execution_state']=='FAILED' and cap['post_run_observations_qualified']
assert "KeyError: 'z4:im'" in cap['stdout_and_stderr']
assert not (HERE/'primary_result.json').exists() and not (HERE/'primary_tables.json.gz').exists()
for name in ['primary_v2.py','replay_v2.py','verify_v2.py','run_v2.py','prepare_v2.py','FAILURE_V1.md']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(raw)
deps=dict(old['input_sha256'])
for p in HERE.iterdir():
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
new=dict(old);new.update({'schema':'SRG1_EXECUTION_PREPARATION_V2','input_sha256':deps,
    'only_mathematical_change':'NORMALIZE_COLON_COMPONENT_ROW_AND_UNDERSCORE_COMPONENT_VARIABLE_NAMES',
    'all_artifact_names_versioned_before_launch':True,'scientific_inputs_or_acceptance_requirements_changed':False})
with (HERE/'execution_preparation_v2.json').open('xb') as out:out.write((json.dumps(new,sort_keys=True,indent=2)+'\n').encode())
print('SRG1_V2_FROZEN',len(deps),'bindings; exact failed V1 preserved',flush=True)
