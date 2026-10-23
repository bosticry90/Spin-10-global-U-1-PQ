"""FAN1 Hermitian transport correction, reusing the completed original primary."""
from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='c4471087732892f1b1101d663d82d3f54b708166'
old=json.loads((HERE/'validation_preparation.json').read_bytes())
for p,h in old['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for role in ['primary','replay']:
    cap=json.loads((HERE/(role+'_capture.json')).read_bytes());v=json.loads((HERE/(role+'_result.json')).read_bytes())
    assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['post_run_observations_qualified']
    out=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert out==[v]
    blob=(HERE/(role+'_tables.json.gz')).read_bytes()
    assert sha256(blob).hexdigest()==v['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==v['tables_sha256']
fail=json.loads((HERE/'validation_capture.json').read_bytes())
assert fail['execution_state']=='FAILED' and fail['exit_code']==1 and 'line 20' in fail['stdout_and_stderr']
assert not (HERE/'validation_receipt.json').exists()
for name in ['replay_v2.py','verify_v2.py','prepare_v2.py','run_v2.py','FAILURE_V1.md']:
    p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    with (HERE/(name+'.source.txt')).open('xb') as out:out.write(raw)
deps=dict(old['input_sha256'])
for p in HERE.iterdir():
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
new=dict(old);new.update({'schema':'FAN1_EXECUTION_PREPARATION_V2','input_sha256':deps,
    'only_correction':'HERMITIAN_FORM_USES_CONJUGATE_TRANSPOSE_UNDER_COMPLEX_BASIS_TRANSPORT',
    'completed_primary_reused_without_rerun':True,'scientific_inputs_or_requirements_changed':False})
with (HERE/'execution_preparation_v2.json').open('xb') as out:out.write((json.dumps(new,sort_keys=True,indent=2)+'\n').encode())
print('FAN1_V2_FROZEN',len(deps),'bindings; completed primary reused',flush=True)
