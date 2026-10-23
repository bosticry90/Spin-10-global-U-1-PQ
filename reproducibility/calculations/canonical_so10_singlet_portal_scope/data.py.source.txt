"""SPS1 IO and point bindings; no shared coefficient derivation."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import gzip,json,os,sys,threading,time
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
PORTALS=['lambdaPhiS','lambdaSigmaS']
CHANGED=['lambdaPhi1','lambdaPhi2','lambdaPhiSigma1','lambdaPhiSigma2','lambdaSigma1','lambdaSigma2','lambdaSigma3','lambdaSigma4','zEta_re','zEta_im']
GATE_FOLDERS={'canonical_so10_singlet_pole_rg_check','canonical_so10_singlet_pole_control','canonical_so10_singlet_quartic_running'}
def begin(role):
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
 assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]))
   if p.parent.resolve()==HERE and p.name.startswith('replay' if role=='primary' else 'primary'):raise PermissionError('SPS1_PEER_DENIED')
   if any(n in p.parts for n in GATE_FOLDERS):raise PermissionError('SPS1_EXPECTED_RESULT_DENIED')
   if role=='replay' and p.name in ['primary_tables.json.gz','replay_tables.json.gz'] and p.parent.name=='canonical_so10_scalar_kernel_reconciliation':raise PermissionError('SPS1_RSC_POLYNOMIAL_DENIED')
 sys.addaudithook(audit);return start
def finish(role,d,start):
 raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
