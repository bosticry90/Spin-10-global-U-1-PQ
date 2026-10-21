from pathlib import Path
from hashlib import sha256
import json
D=Path(__file__).resolve().parent
p=json.loads((D/'preparation.json').read_bytes())
for n,h in p['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
a,b=[json.loads((D/(r+'_result.json')).read_bytes()) for r in ['primary','replay']]
assert a['table_sha256']==b['table_sha256']
for r in ['primary','replay']:
 cap=json.loads((D/(r+'_capture.json')).read_bytes());assert cap['execution_state']=='COMPLETED'
files=list(map(Path,p['input_sha256']))+[D/'preparation.json']
files +=[D/(r+'_'+suffix) for r in ['primary','replay'] for suffix in ['capture.json','result.json','tables.json.gz']]
v={'schema':'C1_BACKGROUND_THRESHOLD_INPUT_VALIDATION_PREPARATION_V1',
'input_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in files}}
with (D/'validation_preparation.json').open('xb') as out:out.write((json.dumps(v,indent=2,sort_keys=True)+'\n').encode())
print('VALIDATION_FROZEN',len(files),flush=True)
