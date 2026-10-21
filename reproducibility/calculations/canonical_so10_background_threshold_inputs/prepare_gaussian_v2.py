from pathlib import Path
from hashlib import sha256
import json
D=Path(__file__).resolve().parent
p=json.loads((D/'validation_preparation.json').read_bytes())
for n,h in p['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
files=list(map(Path,p['input_sha256']))+[D/'validation_preparation.json',D/'validation_capture.json',D/'validation_receipt.json']
for n in ['GAUSSIAN_CONTROL_V2.md','verify_gaussian_v2.py','prepare_gaussian_v2.py','run_gaussian_v2.py']:
 q=D/n
 with (D/(n+'.source.txt')).open('xb') as out:out.write(q.read_bytes())
 files.extend([q,D/(n+'.source.txt')])
v={'schema':'C1_BACKGROUND_THRESHOLD_INPUT_VALIDATION_PREPARATION_V2',
'input_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in files}}
with (D/'validation_preparation_v2.json').open('xb') as out:out.write((json.dumps(v,indent=2,sort_keys=True)+'\n').encode())
print('FROZEN_V2',len(files),flush=True)
