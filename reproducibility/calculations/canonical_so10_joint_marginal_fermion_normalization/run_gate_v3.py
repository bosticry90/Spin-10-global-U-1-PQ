from pathlib import Path
from hashlib import sha256
import json,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/joint-marginal-fermion-normalization-v1-2026-10-23')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
 bind=dict(read(HERE/'validation_preparation.json')['input_sha256'])
 for p,h in bind.items():assert digest(Path(p))==h,p
 assert read(HERE/'primary_capture.json')['exit_code']==read(HERE/'replay_v2_capture.json')['exit_code']==0
 assert read(HERE/'verify_capture.json')['exit_code']==1 and read(HERE/'controller_failure_v2.json')['last_role']=='verify'
 assert not (HERE/'validation_receipt.json').exists() and not (HERE/'joint_selected_family.json.gz').exists()
 for n in ['CONTINUATION_V3.md','verify_v3.py','run_gate_v3.py']:
  p=HERE/n;b=p.read_bytes();assert b'\r' not in b
  if p.suffix=='.py':compile(b,str(p),'exec')
  with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 for p in HERE.iterdir():
  if p.is_file():bind[str(p)]=digest(p)
 dump(HERE/'validation_preparation_v3.json',{'schema':'JMF1_VALIDATION_PREPARATION_V3','input_sha256':bind,'completed_calculations_reused':True,'same_mathematical_acceptance_and_limits':True,'scientific_acceptance':'NOT_PERFORMED'})
 c=capture([sys.executable,'-B',str(HERE/'verify_v3.py')]);dump(HERE/'verify_v3_capture.json',c);dump(CONTROL/'verify_v3_full_capture.json',c);print(c['stdout_and_stderr'],flush=True)
 assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
 assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
 rows=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(rows)==1;r=rows[0]
 assert r['status']=='QUALIFIED_EXACT_ONCE_JOINT_SELECTED_MARGINAL_FERMION_NORMALIZATION' and r['elapsed_after_imports']<600
 dump(HERE/'validation_receipt.json',r);assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<16*1024**2
 print('JMF1_GATE_V3_COMPLETED',flush=True)
except BaseException:
 dump(HERE/'controller_failure_v3.json',{'execution_state':'FAILED','traceback':traceback.format_exc(),'failure_relabelled_PASS':False,'scientific_acceptance':'NOT_PERFORMED'});raise
