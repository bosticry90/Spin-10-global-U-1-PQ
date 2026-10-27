from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/joint-marginal-fermion-normalization-v1-2026-10-23')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
label='preparation_v2'
try:
 p=subprocess.run([sys.executable,'-B',str(HERE/'prepare_v2.py')],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
 pc={'native_exit':p.returncode,'stdout_and_stderr':p.stdout,'scientific_calculations_executed':False}
 dump(HERE/'preparation_v2_capture.json',pc);dump(CONTROL/'preparation_v2_full_capture.json',pc);print(p.stdout,flush=True);assert p.returncode==0
 for label in ['replay_v2','verify']:
  if label=='verify':
   bind=dict(json.loads((HERE/'preparation_v2.json').read_bytes())['input_sha256'])
   for q in HERE.iterdir():
    if q.is_file():bind[str(q)]=sha256(q.read_bytes()).hexdigest()
   dump(HERE/'validation_preparation.json',{'schema':'JMF1_VALIDATION_PREPARATION','input_sha256':bind,'scientific_acceptance':'NOT_PERFORMED'})
  c=capture([sys.executable,'-B',str(HERE/(label+'.py'))]);dump(HERE/(label+'_capture.json'),c);dump(CONTROL/(label+'_full_capture.json'),c);print(c['stdout_and_stderr'],flush=True)
  assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
  assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
  rows=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(rows)==1;r=rows[0];assert r['elapsed_after_imports']<600
  if label=='verify':assert r['status']=='QUALIFIED_EXACT_ONCE_JOINT_SELECTED_MARGINAL_FERMION_NORMALIZATION'
  else:
   raw=(HERE/'replay_tables.json.gz').read_bytes();assert sha256(raw).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(raw)).hexdigest()==r['tables_sha256']
  dump(HERE/('validation_receipt.json' if label=='verify' else label+'_result.json'),r);assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<16*1024**2
  print(label,'COMPLETED',r['elapsed_after_imports'],flush=True)
except BaseException:
 dump(HERE/'controller_failure_v2.json',{'execution_state':'FAILED','last_role':label,'traceback':traceback.format_exc(),'failure_relabelled_PASS':False,'scientific_acceptance':'NOT_PERFORMED'});raise
