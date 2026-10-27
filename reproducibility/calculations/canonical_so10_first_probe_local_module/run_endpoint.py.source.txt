from pathlib import Path
from hashlib import sha256
import gzip,json,subprocess,sys,traceback
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/first-probe-local-module-v1-2026-10-24')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,v):
 with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
stage='endpoint_preparation'
try:
 p=subprocess.run([sys.executable,'-B',str(O/'prepare_endpoint.py')],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');c={'native_exit':p.returncode,'stdout_and_stderr':p.stdout};dump(O/'endpoint_preparation_capture.json',c);dump(C/'endpoint_preparation_full_capture.json',c);print(p.stdout,flush=True);assert p.returncode==0
 for role in ['primary','replay','verify']:
  stage='endpoint_'+role
  if role=='verify':
   b=dict(json.loads((O/'endpoint_preparation.json').read_bytes())['input_sha256'])
   for p in O.iterdir():
    if p.is_file():b[str(p)]=sha256(p.read_bytes()).hexdigest()
   dump(O/'endpoint_validation_preparation.json',{'input_sha256':b})
  cmd=[sys.executable,'-B',str(O/('verify_endpoint.py' if role=='verify' else'endpoint.py'))]+([] if role=='verify' else[role]);c=capture(cmd);dump(O/('endpoint_'+role+'_capture.json'),c);dump(C/('endpoint_'+role+'_full_capture.json'),c)
  assert c['exit_code']==0 and c['execution_state']=='COMPLETED' and c['calculation_completed'] and c['post_run_observations_qualified']
  assert c['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in c['all_resource_samples'])<=8*1024**3
  rr=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<180
  if role!='verify':
   blob=(O/('endpoint_'+role+'_tables.json.gz')).read_bytes();assert sha256(blob).hexdigest()==rr[0]['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==rr[0]['raw_sha256']
  dump(O/('endpoint_validation_receipt.json' if role=='verify' else'endpoint_'+role+'_result.json'),rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<12*1024**2;print('COMPLETED_HP1',role,rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'endpoint_controller_failure.json',{'stage':stage,'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
