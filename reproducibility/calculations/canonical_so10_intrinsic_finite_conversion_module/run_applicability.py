from pathlib import Path
from hashlib import sha256
import json,sys,ast,subprocess,traceback
O=Path(__file__).resolve().parent;R=O.parents[1];C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/intrinsic-finite-conversion-module-v1-2026-10-25');sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'));from export_a10_e5_antighost_vector import capture
def dump(p,z):
 with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 b=dict(json.loads((O/'mass_preparation.json').read_bytes())['input_sha256'])
 for name in ['mass_preparation.json','mass_precheck.json','mass_receipt.json','mass_capture.json']:p=O/name;b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for folder,names in [('canonical_so10_intrinsic_ghost_hatted',['primary_inputs.json.gz','validation_receipt.json','tangent_receipt_v2.json']),('canonical_so10_common_trace_domain',['RESULT.md'])]:
  if folder=='canonical_so10_common_trace_domain':continue
  for name in names:
   p=O.parent/folder/name;assert p.read_bytes()==subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R);b[str(p)]=sha256(p.read_bytes()).hexdigest()
 for name in ['ROOT_APPLICABILITY.md','applicability.py','run_applicability.py']:
  p=O/name
  if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
  with(O/(name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
  b[str(p)]=sha256(p.read_bytes()).hexdigest();b[str(O/(name+'.source.txt'))]=b[str(p)]
 dump(O/'applicability_preparation.json',{'input_sha256':b,'seconds_after_imports':120,'scientific_acceptance':'NOT_PERFORMED'})
 z=capture([sys.executable,'-B',str(O/'applicability.py')]);dump(O/'applicability_capture.json',z);dump(C/'applicability_full_capture.json',z);assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified'];assert z['launch']['memory']['available_pagefile']>=350*1024**2 and max(x['private_bytes'] for x in z['all_resource_samples'])<=8*1024**3
 rr=[json.loads(x[7:]) for x in z['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(rr)==1 and rr[0]['elapsed_after_imports']<120;dump(O/'applicability_receipt.json',rr[0]);assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())<16*1024**2;print('COMPLETED_IFC3',rr[0]['elapsed_after_imports'],flush=True)
except BaseException:
 dump(O/'applicability_controller_failure.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
