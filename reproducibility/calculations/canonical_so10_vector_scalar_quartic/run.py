"""VSP1 sequential color, dependent amplitudes and separate validation captures."""
from pathlib import Path
from hashlib import sha256
import json,sys,gzip
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-scalar-quartic-v1-2026-10-20')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
def auth(prep):
    for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
def resource(c):
    assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed']
    assert c['post_run_observations_qualified'] and c['private_allocation_limit_bytes']==8*1024**3
    assert c['launch']['memory']['available_pagefile']>=350*1024**2
    assert c['all_resource_samples'] and all(0<x['private_bytes']<=8*1024**3 for x in c['all_resource_samples'])
def one(role,kind):
    argv=[sys.executable,'-B',str(HERE/(kind+'.py'))]+([] if kind=='verify' else [role])
    c=capture(argv);name=role+'_'+kind;dump(HERE/(name+'_capture.json'),c);dump(CONTROL/(name+'_full_capture.json'),c)
    if c['execution_state']!='COMPLETED':print(c['stdout_and_stderr'],flush=True)
    resource(c);records=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(records)==1
    value=records[0];assert value['elapsed_after_imports']<300
    dump(HERE/('validation_receipt.json' if kind=='verify' else name+'_result.json'),value)
    print(name,'COMPLETED',value['elapsed_after_imports'],flush=True);return value
prep=json.loads((HERE/'preparation.json').read_bytes());auth(prep)
if sys.argv[1]=='color':
    a=one('primary','color');b=one('replay','color');assert a['tables_sha256']==b['tables_sha256']
    print('ALL20_FULL_COLOR_OPERATORS_AGREE',flush=True)
else:
    names=list(map(Path,prep['input_sha256']))+[HERE/'preparation.json']
    for role in ['primary','replay']:
        resource(json.loads((HERE/(role+'_color_capture.json')).read_bytes()))
        names += [HERE/(role+'_color'+suffix) for suffix in ['_capture.json','_result.json','_tables.json.gz']]
    if sys.argv[1]=='amplitude':
        p={'schema':'VSP1_AMPLITUDE_PREPARATION','input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in sorted(set(names))}}
        dump(HERE/'amplitude_preparation.json',p);auth(p);one('primary','amplitude');one('replay','amplitude')
    else:
        assert sys.argv[1]=='validate';names += [HERE/'amplitude_preparation.json']
        for role in ['primary','replay']:
            resource(json.loads((HERE/(role+'_amplitude_capture.json')).read_bytes()))
            names += [HERE/(role+'_amplitude'+suffix) for suffix in ['_capture.json','_result.json','_tables.json.gz']]
        vp={'schema':'VSP1_VALIDATION_PREPARATION','input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in sorted(set(names))}}
        dump(HERE/'validation_preparation.json',vp);auth(vp);one('validation','verify')
