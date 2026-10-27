from pathlib import Path
from hashlib import sha256
import json,ast,sys,subprocess,traceback
O=Path(__file__).resolve().parent;R=O.parents[1];C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/intrinsic-finite-conversion-module-v1-2026-10-25');sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,z):
 with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 b=dict(json.loads((O/'validation_preparation.json').read_bytes())['input_sha256'])
 for name in ['validation_preparation.json','validation_receipt.json','verify_capture.json']:p=O/name;b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for folder,names in [('canonical_so10_intrinsic_scalar_source_ghost',['yukawa_bridge_inputs.json.gz']),('canonical_so10_intrinsic_regulator_root_v2',['review_receipt.json'])]:
  for name in names:
   p=O.parent/folder/name;assert p.read_bytes()==subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R);b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for name in ['MASS_RECORD.md','mass.py','run_mass.py']:
  p=O/name
  if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
  with(O/(name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
  b[str(p)]=sha256(p.read_bytes()).hexdigest();b[str(O/(name+'.source.txt'))]=b[str(p)]
 dump(O/'mass_preparation.json',{'input_sha256':b,'seconds_after_imports':180,'scientific_acceptance':'NOT_PERFORMED'})
 z=capture([sys.executable,'-B',str(O/'mass.py')]);dump(O/'mass_capture.json',z);dump(C/'mass_full_capture.json',z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3
 rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<180;dump(O/'mass_receipt.json',rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<16*1024**2;print('COMPLETED_IFC2',rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'mass_controller_failure.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
