"""BSR1 exclusive, resource-observed native routes then separate gate."""
from pathlib import Path
from hashlib import sha256
import gzip,json,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/benchmark-scope-reconciliation-v1-2026-10-22')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
assert subprocess.check_output([sys.executable,'-B',str(HERE/'prepare.py')],cwd=ROOT)
def execute(label):
 cap=capture([sys.executable,'-B',str(HERE/(label+'.py'))]);dump(HERE/(label+'_capture.json'),cap);dump(CONTROL/(label+'_full_capture.json'),cap)
 if cap['exit_code']:print(cap['stdout_and_stderr'],flush=True)
 assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
 assert cap['launch']['memory']['available_pagefile']>=350*1024**2 and cap['all_resource_samples'] and max(v['private_bytes'] for v in cap['all_resource_samples'])<=8*1024**3
 out=[json.loads(v[7:]) for v in cap['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(out)==1;r=out[0];assert r['elapsed_after_imports']<600
 if label!='verify':
  b=(HERE/(label+'_tables.json.gz')).read_bytes();assert r['packed_sha256']==sha256(b).hexdigest() and r['tables_sha256']==sha256(gzip.decompress(b)).hexdigest();dump(HERE/(label+'_result.json'),r)
 else:
  assert r['status']=='QUALIFIED_DISTINCT_REFERENCE_SCOPES_AND_NAVIGATION_CORRECTION';dump(HERE/'validation_receipt.json',r)
 assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
 print(label,'COMPLETED',r['elapsed_after_imports'],flush=True)
label=None
try:
 for label in ['primary','replay']:execute(label)
 d=json.loads((HERE/'preparation.json').read_bytes());bind=dict(d['input_sha256'])
 for p in HERE.iterdir():
  if p.is_file():bind[str(p)]=sha256(p.read_bytes()).hexdigest()
 dump(HERE/'validation_preparation.json',{'schema':'BSR1_VALIDATION_PREPARATION','input_sha256':bind,'scientific_acceptance':'NOT_PERFORMED'})
 label='verify';execute(label)
except BaseException:
 dump(HERE/'controller_failure.json',{'execution_state':'FAILED','last_role':label,'traceback':traceback.format_exc(),'scientific_acceptance':'NOT_PERFORMED','failure_relabelled_PASS':False});raise
