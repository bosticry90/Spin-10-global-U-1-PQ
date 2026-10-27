from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/double-source-finite-ward-v1-2026-10-24')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
label='preparation'
try:
 p=subprocess.run([sys.executable,'-B',str(HERE/'prepare.py')],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');c={'native_exit':p.returncode,'stdout_and_stderr':p.stdout,'scientific_calculations_executed':False};dump(HERE/'preparation_capture.json',c)
 if CONTROL.exists():dump(CONTROL/'preparation_full_capture.json',c)
 print(p.stdout,flush=True);assert p.returncode==0
 for role in ['primary','replay','verify']:
  label=role
  if role=='verify':
   b=dict(json.loads((HERE/'preparation.json').read_bytes())['input_sha256'])
   for f in HERE.iterdir():
    if f.is_file():b[str(f)]=sha256(f.read_bytes()).hexdigest()
   dump(HERE/'validation_preparation.json',{'input_sha256':dict(sorted(b.items())),'scientific_acceptance':'NOT_PERFORMED'})
  c=capture([sys.executable,'-B',str(HERE/(role+'.py'))]);dump(HERE/(role+'_capture.json'),c);dump(CONTROL/(role+'_full_capture.json'),c);print(c['stdout_and_stderr'],flush=True)
  assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
  assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
  rr=[json.loads(z[7:]) for z in c['stdout_and_stderr'].splitlines() if z.startswith('RESULT ')];assert len(rr)==1;r=rr[0];assert r['elapsed_after_imports']<600
  if role!='verify':
   b=(HERE/(role+'_tables.json.gz')).read_bytes();assert sha256(b).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(b)).hexdigest()==r['tables_sha256'];dump(HERE/(role+'_result.json'),r)
  else:
   b=(HERE/'selected_contact_Ward_descendants.json.gz').read_bytes();assert sha256(b).hexdigest()==r['artifact_sha256'] and sha256(gzip.decompress(b)).hexdigest()==r['artifact_raw_sha256'];dump(HERE/'validation_receipt.json',r)
  assert sum(f.stat().st_size for f in HERE.iterdir() if f.is_file())<16*1024**2
except BaseException:
 dump(HERE/'controller_failure.json',{'execution_state':'FAILED','last_role':label,'traceback':traceback.format_exc(),'failure_relabelled_PASS':False,'scientific_acceptance':'NOT_PERFORMED'});raise
