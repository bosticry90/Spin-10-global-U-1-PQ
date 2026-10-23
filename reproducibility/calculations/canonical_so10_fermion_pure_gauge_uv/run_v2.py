"""GPC1 V2 freezes preserved failure and reuses completed P/R bytes."""
from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/fermion-pure-gauge-uv-v1-2026-10-22')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
bind=dict(read(HERE/'validation_preparation.json')['input_sha256'])
for n,h in bind.items():assert digest(Path(n))==h,n
assert read(HERE/'verify_capture.json')['exit_code']==1 and read(HERE/'controller_failure.json')['execution_state']=='FAILED'
for n in ['primary','replay']:
 cap=read(HERE/(n+'_capture.json'));result=read(HERE/(n+'_result.json'));blob=(HERE/(n+'_tables.json.gz')).read_bytes()
 assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and sha256(blob).hexdigest()==result['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==result['tables_sha256']
for n in ['CONTINUATION_V2.md','verify_v2.py','run_v2.py']:
 f=HERE/n;raw=f.read_bytes();assert b'\r' not in raw
 if f.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as h:h.write(raw)
for f in HERE.iterdir():
 if f.is_file():bind[str(f)]=digest(f)
dump(HERE/'validation_preparation_v2.json',{'schema':'GPC1_VALIDATION_PREPARATION_V2','input_sha256':bind,'completed_loop_workers_rerun':False,'scientific_acceptance':'NOT_PERFORMED'})
try:
 cap=capture([sys.executable,'-B',str(HERE/'verify_v2.py')]);dump(HERE/'verify_v2_capture.json',cap);dump(CONTROL/'verify_v2_full_capture.json',cap)
 if cap['exit_code']:print(cap['stdout_and_stderr'],flush=True)
 assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and cap['calculation_completed'] and cap['post_run_observations_qualified']
 assert cap['launch']['memory']['available_pagefile']>=350*1024**2 and cap['all_resource_samples'] and max(v['private_bytes'] for v in cap['all_resource_samples'])<=8*1024**3
 rows=[json.loads(v[7:]) for v in cap['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(rows)==1;r=rows[0];assert r['elapsed_after_imports']<600 and r['status']=='QUALIFIED_COMPLETE_PARITY_EVEN_MASS_INDEPENDENT_PURE_GAUGE_FERMION_UV_FUNCTIONAL'
 dump(HERE/'validation_receipt_v2.json',r);assert sum(f.stat().st_size for f in HERE.iterdir() if f.is_file())<16*1024**2
 print('VERIFY_V2_COMPLETED '+json.dumps(r,sort_keys=True),flush=True)
except BaseException:
 dump(HERE/'controller_failure_v2.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
