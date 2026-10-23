"""SRM1 sequential observed runs; complete capture before qualification checks."""
from pathlib import Path
from hashlib import sha256
import gzip,json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/source-region-matching-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,value):
    with p.open('xb') as f:f.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
prep=HERE/'preparation.json'
for p,h in json.loads(prep.read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
roles=[('primary','primary.py'),('replay','replay.py'),('validation','verify.py')]
outputs=['validation_preparation.json','validation_receipt.json','controller_failure.json']
for role,_ in roles:
    outputs.append(role+'_capture.json')
    if role!='validation':outputs.extend([role+'_result.json',role+'_tables.json.gz'])
for n in outputs:assert not (HERE/n).exists(),n
for role,_ in roles:assert not (CONTROL/(role+'_full_capture.json')).exists(),role
role=None
try:
    for role,worker in roles:
        if role=='validation':
            deps=dict(json.loads(prep.read_bytes())['input_sha256'])
            for p in HERE.iterdir():
                if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
            dump(HERE/'validation_preparation.json',{'schema':'SRM1_VALIDATION_PREPARATION','input_sha256':deps,'seconds':600,'scientific_acceptance':'NOT_PERFORMED'})
        cap=capture([sys.executable,'-B',str(HERE/worker)])
        dump(HERE/(role+'_capture.json'),cap);dump(CONTROL/(role+'_full_capture.json'),cap)
        if cap['exit_code']!=0:print(cap['stdout_and_stderr'],flush=True)
        assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
        assert cap['launch']['memory']['available_pagefile']>=350*1024**2
        assert cap['all_resource_samples'] and all(x['private_bytes']<=8*1024**3 for x in cap['all_resource_samples'])
        results=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')]
        assert len(results)==1;result=results[0];assert result['elapsed_after_imports']<600
        if role=='validation':
            assert result['status']=='QUALIFIED_FORMAL_SOURCE_REGION_MATCHING_AND_LOCAL_BOSONIC_WIDTH_IDENTITY'
            dump(HERE/'validation_receipt.json',result)
        else:
            assert result['role']==role;blob=(HERE/(role+'_tables.json.gz')).read_bytes()
            assert sha256(blob).hexdigest()==result['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==result['tables_sha256']
            dump(HERE/(role+'_result.json'),result)
        assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
        print(role,'COMPLETED',result['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure.json',{'execution_state':'FAILED','last_role':role,'traceback':traceback.format_exc(),
        'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
