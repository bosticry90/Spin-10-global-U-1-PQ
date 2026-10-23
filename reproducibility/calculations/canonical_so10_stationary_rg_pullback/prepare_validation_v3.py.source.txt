"""SRG1 authenticate completed V2 natives and freeze only verifier correction."""
from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='45352e8d446f60000c1caaa1900e03317e1f78e4'
old=json.loads((HERE/'validation_preparation_v2.json').read_bytes())
for p,h in old['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for role in ['primary_v2','replay_v2']:
    cap=json.loads((HERE/(role+'_capture.json')).read_bytes());v=json.loads((HERE/(role+'_result.json')).read_bytes())
    assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['post_run_observations_qualified']
    result=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert result==[v]
    blob=(HERE/(role+'_tables.json.gz')).read_bytes()
    assert sha256(blob).hexdigest()==v['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==v['tables_sha256']
fail=json.loads((HERE/'validation_v2_capture.json').read_bytes())
assert fail['execution_state']=='FAILED' and fail['exit_code']==1 and 'line 77' in fail['stdout_and_stderr']
assert not (HERE/'validation_receipt_v2.json').exists()
for name in ['verify_v3.py','prepare_validation_v3.py','run_validation_v3.py','CORRECTION_V3.md']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(raw)
deps=dict(old['input_sha256'])
for p in HERE.iterdir():
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
new=dict(old);new.update({'schema':'SRG1_VALIDATION_PREPARATION_V3','input_sha256':deps,
    'completed_V2_natives_reused_without_rerun':True,'only_correction':'EXACT_NUMERIC_ZERO_INSTEAD_OF_SERIALIZED_STRING_IDENTITY',
    'scientific_inputs_or_acceptance_requirements_changed':False})
with (HERE/'validation_preparation_v3.json').open('xb') as out:out.write((json.dumps(new,sort_keys=True,indent=2)+'\n').encode())
print('SRG1_VALIDATION_V3_FROZEN',len(deps),'bindings; native reruns0',flush=True)
