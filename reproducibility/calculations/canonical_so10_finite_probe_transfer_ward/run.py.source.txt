from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,sys,traceback
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/finite-probe-transfer-ward-v1-2026-10-25');sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,v):
 with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
stage='preparation'
try:
 p=subprocess.run([sys.executable,'-B',str(O/'prepare.py')],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');z={'native_exit':p.returncode,'stdout_and_stderr':p.stdout};dump(O/'preparation_capture.json',z);dump(C/'preparation_full_capture.json',z);assert p.returncode==0
 for role in ['primary','replay','verify']:
  stage=role
  if role=='verify':
   b=dict(json.loads((O/'preparation.json').read_bytes())['input_sha256']);F=O.parent/'canonical_so10_probe_fermion_onejet';m=json.loads((F/'construction_validation_preparation.json').read_bytes())['input_sha256'];p=F/'construction_tables.json.gz';assert sha256(p.read_bytes()).hexdigest()==m[str(p)]
   for p in [p,F/'construction_validation_preparation.json',O/'preparation.json',O/'preparation_capture.json',O/'primary_result.json',O/'primary_capture.json',O/'primary_tables.json.gz',O/'replay_result.json',O/'replay_capture.json',O/'replay_tables.json.gz']:b[str(p)]=sha256(p.read_bytes()).hexdigest()
   dump(O/'validation_preparation.json',{'input_sha256':b,'explicit_file_list':True})
  z=capture([sys.executable,'-B',str(O/('verify.py' if role=='verify' else'native.py'))]+([] if role=='verify' else[role]));dump(O/(role+'_capture.json'),z);dump(C/(role+'_full_capture.json'),z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3;rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<180
  if role!='verify':
   blob=(O/(role+'_tables.json.gz')).read_bytes();assert sha256(blob).hexdigest()==rr[0]['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==rr[0]['raw_sha256']
  dump(O/('validation_receipt.json' if role=='verify' else role+'_result.json'),rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<12*1024**2;print('COMPLETED_NVT1',role,rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'controller_failure.json',{'execution_state':'FAILED','stage':stage,'traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
