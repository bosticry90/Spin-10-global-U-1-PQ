"""Sequential native runs, exact captures before resource/science assertions."""
from pathlib import Path
from hashlib import sha256
import json,sys,subprocess,os
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/background-threshold-inputs-v1-2026-10-20')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
from audit_a10_e5_antighost_vector import resource,line_json
prep=json.loads((D/'preparation.json').read_bytes())
for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
query="@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.ProcessId -ne "+str(os.getpid())+" -and $_.CommandLine -like '*canonical_so10_background_threshold_inputs*' } | Select-Object ProcessId,CommandLine) | ConvertTo-Json -Compress"
assert not subprocess.check_output(['pwsh','-NoProfile','-Command',query]).strip(),'LIVE_WORK_PRESERVE_HANDLE'
for role in ['primary','replay']:
 cap=capture([sys.executable,'-B',str(D/'pilot.py'),role]);raw=(json.dumps(cap,sort_keys=True,separators=(',',':'))+'\n').encode()
 for dest in [D/(role+'_capture.json'),C/(role+'_full_capture.json')]:
  with dest.open('xb') as f:f.write(raw)
 if cap['execution_state']!='COMPLETED':print(cap['stdout_and_stderr'],flush=True)
 resource(cap);v=line_json(cap['stdout_and_stderr'],'RESULT ');assert v['elapsed_after_imports']<120
 with (D/(role+'_result.json')).open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
 print(role,'COMPLETED',v['elapsed_after_imports'],'T',v['tensor_nonzero'],flush=True)
