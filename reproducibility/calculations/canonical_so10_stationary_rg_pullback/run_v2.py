"""SRG1 exclusive observed routes; retain a genuine finite-scale mismatch."""
from pathlib import Path
from hashlib import sha256
import gzip,json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/stationary-rg-pullback-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
prep=HERE/'execution_preparation_v2.json'
for p,h in json.loads(prep.read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
routes=[('primary_v2','primary_v2.py'),('replay_v2','replay_v2.py'),('validation_v2','verify_v2.py')]
prospective=['validation_preparation_v2.json','validation_receipt_v2.json','controller_failure_v2.json']
for role,_ in routes:
    prospective.append(role+'_capture.json')
    if role!='validation_v2':prospective.extend([role+'_result.json',role+'_tables.json.gz'])
for n in prospective:assert not (HERE/n).exists(),n
for role,_ in routes:assert not (CONTROL/(role+'_full_capture.json')).exists(),role
role=None
try:
    for role,worker in routes:
        if role=='validation_v2':
            deps=dict(json.loads(prep.read_bytes())['input_sha256'])
            for p in HERE.iterdir():
                if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
            dump(HERE/'validation_preparation_v2.json',{'schema':'SRG1_VALIDATION_PREPARATION_V2','input_sha256':deps,'seconds':600,'scientific_acceptance':'NOT_PERFORMED'})
        c=capture([sys.executable,'-B',str(HERE/worker)]);dump(HERE/(role+'_capture.json'),c);dump(CONTROL/(role+'_full_capture.json'),c)
        if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
        assert c['launch']['memory']['available_pagefile']>=350*1024**2
        assert c['all_resource_samples'] and all('private_bytes' in x and x['private_bytes']<=8*1024**3 for x in c['all_resource_samples'])
        results=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')]
        assert len(results)==1 and results[0]['elapsed_after_imports']<600;result=results[0]
        if role=='validation_v2':
            assert result['status'] in ['QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_AND_SCOPED_SCALE_IDENTITY','QUALIFIED_STATIONARY_PARENT_RG_PULLBACK_WITH_FINITE_SCALE_MISMATCH']
            dump(HERE/'validation_receipt_v2.json',result)
        else:
            assert result['role']==role;blob=(HERE/(role+'_tables.json.gz')).read_bytes()
            assert sha256(blob).hexdigest()==result['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==result['tables_sha256']
            dump(HERE/(role+'_result.json'),result)
        assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
        print(role,'COMPLETED',result['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure_v2.json',{'execution_state':'FAILED','last_role':role,'traceback':traceback.format_exc(),'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
