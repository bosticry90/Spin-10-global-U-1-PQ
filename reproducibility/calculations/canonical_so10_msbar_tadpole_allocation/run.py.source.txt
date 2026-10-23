"""MTA1 observed native routes and subsequent independent validation."""
from pathlib import Path
from hashlib import sha256
import gzip,json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/msbar-tadpole-allocation-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
for p,h in json.loads((HERE/'preparation.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
role=None
try:
    for role in ['primary','replay','validation']:
        if role=='validation':
            deps=dict(json.loads((HERE/'preparation.json').read_bytes())['input_sha256'])
            for p in HERE.iterdir():
                if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
            dump(HERE/'validation_preparation.json',{'schema':'MTA1_VALIDATION_PREPARATION','input_sha256':deps,'seconds':600,'scientific_acceptance':'NOT_PERFORMED'})
        worker=HERE/('verify.py' if role=='validation' else role+'.py')
        c=capture([sys.executable,'-B',str(worker)]);dump(HERE/(role+'_capture.json'),c);dump(CONTROL/(role+'_full_capture.json'),c)
        if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
        assert c['launch']['memory']['available_pagefile']>=350*1024**2
        assert all('private_bytes' in v and v['private_bytes']<=8*1024**3 for v in c['all_resource_samples'])
        out=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(out)==1 and out[0]['elapsed_after_imports']<600
        if role=='validation':
            assert out[0]['status']=='QUALIFIED_MSBAR_PARENT_CONSTRAINT_AND_CORRELATED_RADIAL_TADPOLE_ALLOCATION'
            dump(HERE/'validation_receipt.json',out[0])
        else:
            blob=(HERE/(role+'_tables.json.gz')).read_bytes()
            assert sha256(blob).hexdigest()==out[0]['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==out[0]['tables_sha256']
            dump(HERE/(role+'_result.json'),out[0])
        assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
        print(role,'COMPLETED',out[0]['elapsed_after_imports'],flush=True)
except BaseException:
    dump(HERE/'controller_failure.json',{'execution_state':'FAILED','last_role':role,'traceback':traceback.format_exc(),
        'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
