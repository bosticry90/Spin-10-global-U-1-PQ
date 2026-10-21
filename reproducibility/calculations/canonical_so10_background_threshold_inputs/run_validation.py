from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/background-threshold-inputs-v1-2026-10-20')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
from audit_a10_e5_antighost_vector import resource,line_json
cap=capture([sys.executable,'-B',str(D/'verify.py')]);raw=(json.dumps(cap,sort_keys=True,separators=(',',':'))+'\n').encode()
for dest in [D/'validation_capture.json',C/'validation_full_capture.json']:
 with dest.open('xb') as f:f.write(raw)
if cap['execution_state']!='COMPLETED':print(cap['stdout_and_stderr'],flush=True)
resource(cap);v=line_json(cap['stdout_and_stderr'],'RESULT ');assert v['elapsed_after_imports']<180
with (D/'validation_receipt.json').open('xb') as f:f.write((json.dumps(v,indent=2,sort_keys=True)+'\n').encode())
print('VALIDATED',v['elapsed_after_imports'],flush=True)
