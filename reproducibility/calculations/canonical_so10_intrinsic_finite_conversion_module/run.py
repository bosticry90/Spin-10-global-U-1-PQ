from pathlib import Path
from hashlib import sha256
import json,subprocess,sys,traceback
O=Path(__file__).resolve().parent;R=O.parents[1];C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/intrinsic-finite-conversion-module-v1-2026-10-25');sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,z):
 with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 p=subprocess.run([sys.executable,'-B',str(O/'prepare.py')],cwd=R,capture_output=True);z={'native_exit':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()};dump(O/'preparation_capture.json',z);dump(C/'preparation_full_capture.json',z);assert p.returncode==0
 for role in ['primary','replay','verify']:
  if role=='verify':
   b=dict(json.loads((O/'preparation.json').read_bytes())['input_sha256'])
   for name in ['preparation.json']+[r+s for r in ['primary','replay'] for s in ['_tables.json.gz','_result.json','_capture.json']]:p=O/name;b[str(p)]=sha256(p.read_bytes()).hexdigest()
   dump(O/'validation_preparation.json',{'input_sha256':b,'seconds_after_imports':180,'scientific_acceptance':'NOT_PERFORMED'})
  command=[sys.executable,'-B',str(O/('verify.py' if role=='verify' else'native.py'))]+([] if role=='verify' else[role]);z=capture(command);dump(O/(role+'_capture.json'),z);dump(C/(role+'_full_capture.json'),z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3
  rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<(180 if role=='verify' else300);dump(O/('validation_receipt.json' if role=='verify' else role+'_result.json'),rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<16*1024**2;print('COMPLETED_IFC1',role,rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'controller_failure.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
