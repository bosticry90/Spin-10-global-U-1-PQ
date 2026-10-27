from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vacuum-heat-root-completion-v1-2026-10-24')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode())
label='preparation_v5'
try:
 p=subprocess.run([sys.executable,'-B',str(HERE/'prepare_v5.py')],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');pc={'native_exit':p.returncode,'stdout_and_stderr':p.stdout,'scientific_calculations_executed':False};dump(HERE/'preparation_v5_capture.json',pc);dump(CONTROL/'preparation_v5_full_capture.json',pc);print(p.stdout,flush=True);assert p.returncode==0
 label='integrate_v5';c=capture([sys.executable,'-B',str(HERE/'integrate_v5.py')]);dump(HERE/'integrate_v5_capture.json',c);dump(CONTROL/'integrate_v5_full_capture.json',c);print(c['stdout_and_stderr'],flush=True)
 assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
 assert c['launch']['memory']['available_pagefile']>=350*1024**2 and c['all_resource_samples'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
 rows=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(rows)==1;r=rows[0];assert r['elapsed_after_imports']<600 and r['status']=='QUALIFIED_EXACT_ONCE_SELECTED_JOINT_VACUUM_TANGENT_EXTENSION'
 blob=(HERE/'selected_joint_vacuum_extension_v5.json.gz').read_bytes();assert sha256(blob).hexdigest()==r['artifact_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['artifact_raw_sha256']
 dump(HERE/'joint_receipt_v5.json',r);assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<16*1024**2
except BaseException:
 dump(HERE/'controller_failure_v5.json',{'execution_state':'FAILED','last_role':label,'traceback':traceback.format_exc(),'failure_relabelled_PASS':False,'scientific_acceptance':'NOT_PERFORMED'});raise
