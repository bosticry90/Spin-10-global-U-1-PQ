"""MGN1 sequential observed complete coefficient routes and separate verifier."""
from pathlib import Path
from hashlib import sha256
import gzip,json,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/matter-gauge-vertex-normalization-v1-2026-10-22')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
assert subprocess.check_output([sys.executable,'-B',str(HERE/'prepare.py')],cwd=ROOT)
origin=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/yukawa-dependent-gauge-vertices-v1-2026-10-22')
source={}
for n in ['readiness.jsonl','readiness_stderr.txt']:
 blob=(origin/n).read_bytes();source[str(origin/n)]=sha256(blob).hexdigest()
 with (CONTROL/n).open('xb') as f:f.write(blob)
events=[json.loads(x) for x in (CONTROL/'readiness.jsonl').read_text().splitlines()];steps=[x for x in events if x['event']=='step_finished'];assert [x['exit_code'] for x in steps]==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED'
dump(CONTROL/'readiness_reuse.json',{'source_sha256':source,'fresh_readiness_execution_here':False,'source_was_fresh_in_this_logical_goal_turn':True,'custody':'EXIT2_SEVEN_NOTPASS'})
print('AUTHENTICATED_READINESS_REUSE',flush=True)

def execute(label):
 cap=capture([sys.executable,'-B',str(HERE/(label+'.py'))]);dump(HERE/(label+'_capture.json'),cap);dump(CONTROL/(label+'_full_capture.json'),cap)
 if cap['exit_code']:print(cap['stdout_and_stderr'],flush=True)
 assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
 assert cap['launch']['memory']['available_pagefile']>=350*1024**2 and cap['all_resource_samples'] and max(v['private_bytes'] for v in cap['all_resource_samples'])<=8*1024**3
 rows=[json.loads(v[7:]) for v in cap['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(rows)==1;r=rows[0];assert r['elapsed_after_imports']<600
 if label!='verify':
  blob=(HERE/(label+'_tables.json.gz')).read_bytes();assert sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256'];dump(HERE/(label+'_result.json'),r)
 else:
  assert r['status'] in ['QUALIFIED_COMPLETE_PROPER_FERMION_GAUGE_VERTEX_UV_AND_FIXED_NORMALIZATION_PROJECTION','QUALIFIED_COMPLETE_VERTEX_UV_WITH_FIXED_NORMALIZATION_REMAINDER'];dump(HERE/'validation_receipt.json',r)
 assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<16*1024**2
 print(label,'COMPLETED',r['elapsed_after_imports'],flush=True)
label=None
try:
 for label in ['primary','replay']:execute(label)
 bind=dict(json.loads((HERE/'preparation.json').read_bytes())['input_sha256'])
 for p in HERE.iterdir():
  if p.is_file():bind[str(p)]=sha256(p.read_bytes()).hexdigest()
 dump(HERE/'validation_preparation.json',{'schema':'MGN1_VALIDATION_PREPARATION','input_sha256':bind,'scientific_acceptance':'NOT_PERFORMED'})
 label='verify';execute(label)
except BaseException:
 dump(HERE/'controller_failure.json',{'execution_state':'FAILED','last_role':label,'traceback':traceback.format_exc(),'failure_relabelled_PASS':False,'scientific_acceptance':'NOT_PERFORMED'});raise
