from pathlib import Path
from hashlib import sha256
import json,sys,ast,traceback
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/chiral-scalar-bubble-joint-fp-v1-2026-10-25');H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,v):
 with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 for n in ['preparation.json','validation_preparation.json']:
  for p,h in read(O/n)['input_sha256'].items():assert H(Path(p))==h,p
 for n in ['REVIEW.md','review.py','run_review.py']:
  p=O/n
  if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
  with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b=dict(read(O/'validation_preparation.json')['input_sha256']);b.update({str(p):H(p) for p in O.iterdir() if p.is_file()});dump(O/'review_preparation.json',{'input_sha256':b,'scientific_acceptance':'NOT_PERFORMED'})
 z=capture([sys.executable,'-B',str(O/'review.py')]);dump(O/'review_capture.json',z);dump(C/'review_full_capture.json',z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3;rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<180;dump(O/'review_receipt.json',rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<8*1024**2;print('COMPLETED_SBJ1_REVIEW',rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'review_failure.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
