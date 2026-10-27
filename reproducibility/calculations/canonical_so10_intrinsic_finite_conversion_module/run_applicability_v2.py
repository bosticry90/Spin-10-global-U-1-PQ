from pathlib import Path
from hashlib import sha256
import json,sys,ast,subprocess,traceback
O=Path(__file__).resolve().parent;R=O.parents[1];C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/intrinsic-finite-conversion-module-v1-2026-10-25');sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,z):
 with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 b=dict(json.loads((O/'applicability_preparation.json').read_bytes())['input_sha256'])
 for name in ['applicability_preparation.json','applicability_capture.json','applicability_controller_failure.json','applicability_failure_diagnostic.json']:p=O/name;b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for name in ['RESULT.md','DERIVATION_V2.md','validation_receipt.json']:
  p=O.parent/'canonical_so10_joint_born_ir_trace_domain'/name;assert p.read_bytes()==subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R);b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for name in ['ROOT_APPLICABILITY_CONTINUATION_V2.md','applicability_v2.py','run_applicability_v2.py']:
  p=O/name
  if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
  with(O/(name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
  b[str(p)]=sha256(p.read_bytes()).hexdigest();b[str(O/(name+'.source.txt'))]=b[str(p)]
 dump(O/'applicability_preparation_v2.json',{'input_sha256':b,'seconds_after_imports':120,'scientific_acceptance':'NOT_PERFORMED'})
 z=capture([sys.executable,'-B',str(O/'applicability_v2.py')]);dump(O/'applicability_v2_capture.json',z);dump(C/'applicability_v2_full_capture.json',z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3
 rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<120;dump(O/'applicability_receipt_v2.json',rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<16*1024**2;print('COMPLETED_IFC3_V2',rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'applicability_v2_controller_failure.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
