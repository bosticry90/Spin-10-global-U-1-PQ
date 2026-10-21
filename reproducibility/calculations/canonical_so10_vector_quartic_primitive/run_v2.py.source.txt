"""Frozen sequential native routes, comparison, and independent validation."""
from pathlib import Path
from hashlib import sha256
import json,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-quartic-primitive-v1-2026-10-20')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,value):
    with p.open('xb') as out:out.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
def auth(p):
    for n,h in p['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
def resource(c):
    assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed']
    assert c['post_run_observations_qualified'] and c['private_allocation_limit_bytes']==8*1024**3
    assert c['launch']['memory']['available_pagefile']>=350*1024**2
    assert c['all_resource_samples'] and all(0<x['private_bytes']<=8*1024**3 for x in c['all_resource_samples'])
def one(role,script,args):
    c=capture([sys.executable,'-B',str(HERE/script),*args])
    dump(HERE/(role+'_v2_capture.json'),c);dump(CONTROL/(role+'_v2_full_capture.json'),c)
    if c['execution_state']!='COMPLETED':print(c['stdout_and_stderr'],flush=True)
    resource(c)
    values=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(values)==1
    value=values[0];assert value['elapsed_after_imports']<(240 if role=='validation' else 180)
    dump(HERE/('validation_receipt_v2.json' if role=='validation' else role+'_v2_result.json'),value)
    print(role,'COMPLETED',value['elapsed_after_imports'],flush=True);return value
prep=json.loads((HERE/'preparation_v2.json').read_bytes());auth(prep)
if sys.argv[1]=='native':
    a=one('primary','primitive_v2.py',['primary']);b=one('replay','primitive_v2.py',['replay'])
    assert a['tables_sha256']==b['tables_sha256'] and a['packed_sha256']==b['packed_sha256']
    print('ALL_EXACT_TABLES_AND_LAURENT_COEFFICIENTS_AGREE',flush=True)
else:
    assert sys.argv[1]=='validate';names=list(map(Path,prep['input_sha256']))+[HERE/'preparation_v2.json']
    for role in ['primary','replay']:
        resource(json.loads((HERE/(role+'_v2_capture.json')).read_bytes()))
        names += [HERE/(role+suffix) for suffix in ['_v2_capture.json','_v2_result.json','_v2_tables.json.gz']]
    vp={'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_VALIDATION_PREPARATION_V1',
        'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in sorted(set(names))}}
    dump(HERE/'validation_preparation_v2.json',vp);auth(vp);one('validation','verify_v2.py',[])
