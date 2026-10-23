"""Freeze V3 with separate exclusive artifacts after two preserved failures."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='e94b6f59fbf7f933f273a46b6a1364f348005029'
old=json.loads((HERE/'execution_preparation_v2.json').read_bytes())
for n,h in old['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
assert (HERE/'primary_tables.json.gz').is_file() and not (HERE/'primary_result.json').exists()
failure=json.loads((HERE/'controller_failure_v2.json').read_bytes())
assert failure['execution_state']=='FAILED' and 'FileExistsError' in failure['traceback']
for name in ['primary_v3.py','replay_v3.py','verify_v3.py','run_v3.py','prepare_v3.py','CONTROLLER_FAILURE_V2.md']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(raw)
deps=dict(old['input_sha256'])
for p in HERE.iterdir():
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
new=dict(old);new.update({'schema':'MTA1_EXECUTION_PREPARATION_V3','input_sha256':deps,
    'only_new_correction':'EXPLICIT_UNIQUE_V3_ARTIFACT_NAMES_BEFORE_LAUNCH',
    'V2_table_status':'UNQUALIFIED_NATIVE_TABLE_WITHOUT_COMPLETE_SAVED_CAPTURE',
    'scientific_inputs_or_requirements_changed':False})
with (HERE/'execution_preparation_v3.json').open('xb') as out:out.write((json.dumps(new,sort_keys=True,indent=2)+'\n').encode())
print('MTA1_V3_FROZEN',len(deps),'bindings; V1/V2 failures preserved',flush=True)
