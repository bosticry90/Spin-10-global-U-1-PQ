"""FAN1 corrected replay plus separate verifier, never overwriting V1."""
from pathlib import Path
from hashlib import sha256
import gzip,json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/finite-assembly-nielsen-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
prep=HERE/'execution_preparation_v2.json'
for p,h in json.loads(prep.read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
for name in ['replay_v2_tables.json.gz','replay_v2_capture.json','replay_v2_result.json','validation_preparation_v2.json','validation_v2_capture.json','validation_receipt_v2.json','controller_failure_v2.json']:assert not (HERE/name).exists(),name
for role in ['replay_v2','validation_v2']:assert not (CONTROL/(role+'_full_capture.json')).exists(),role
role=None
try:
    for role,worker in [('replay_v2','replay_v2.py'),('validation_v2','verify_v2.py')]:
        if role=='validation_v2':
            deps=dict(json.loads(prep.read_bytes())['input_sha256'])
            for p in HERE.iterdir():
                if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
            dump(HERE/'validation_preparation_v2.json',{'schema':'FAN1_VALIDATION_PREPARATION_V2','input_sha256':deps,'seconds':600,'scientific_acceptance':'NOT_PERFORMED'})
        cap=capture([sys.executable,'-B',str(HERE/worker)]);dump(HERE/(role+'_capture.json'),cap);dump(CONTROL/(role+'_full_capture.json'),cap)
        if cap['exit_code']!=0:print(cap['stdout_and_stderr'],flush=True)
        assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
        assert cap['launch']['memory']['available_pagefile']>=350*1024**2 and cap['all_resource_samples']
        assert all('private_bytes' in x and x['private_bytes']<=8*1024**3 for x in cap['all_resource_samples'])
        out=[json.loads(x[7:]) for x in cap['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(out)==1 and out[0]['elapsed_after_imports']<600
        result=out[0]
        if role=='validation_v2':
            assert result['status']=='QUALIFIED_FIXED_XI_FINITE_BOSONIC_ASSEMBLY_AND_FIRST_NIELSEN_KERNEL';dump(HERE/'validation_receipt_v2.json',result)
        else:
            assert result['role']=='replay_v2';blob=(HERE/'replay_v2_tables.json.gz').read_bytes()
            assert sha256(blob).hexdigest()==result['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==result['tables_sha256'];dump(HERE/'replay_v2_result.json',result)
        assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
        print(role,'COMPLETED',result['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure_v2.json',{'execution_state':'FAILED','last_role':role,'traceback':traceback.format_exc(),'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
