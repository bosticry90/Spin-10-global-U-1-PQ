"""BSR1 selected reference metadata; no old mathematical worker imported."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import ast,gzip,json,os,sys,threading,time
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
NAMES=['lambdaPhi1','lambdaPhi2','lambdaPhiSigma1','lambdaPhiSigma2','lambdaSigma1','lambdaSigma2','lambdaSigma3','lambdaSigma4']
OLD_POINT='calculations/canonical_so10_positive_higgs/POINT.json'
FINITE_POINT='calculations/canonical_so10_coherent_joint_witness/POINT.json'
RECEIPTS={
 'search':('canonical_so10_bounded_scalar_feasibility','validation_receipt.json'),
 'eta_exclusion':('canonical_so10_eta_offdiagonal_bound','validation_receipt.json'),
 'finite_witness':('canonical_so10_coherent_joint_witness','validation_receipt.json'),
 'finite_contact':('canonical_so10_complete_contact_bound','validation_receipt.json'),
 'finite_BFB':('canonical_so10_finite_full_bfb','validation_receipt.json'),
 'finite_scalar_warning':('canonical_so10_finite_radial_control','validation_receipt.json'),
 'finite_bosonic_warning':('canonical_so10_finite_radial_control','bosonic_validation_receipt.json'),
 'finite_input_warning':('canonical_so10_finite_physical_input_screen','validation_receipt.json')}
def begin(role):
 start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
 assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]))
   if p.parent.resolve()==HERE and p.name.startswith('replay' if role=='primary' else 'primary'):raise PermissionError('BSR1_PEER_DENIED')
 sys.addaudithook(audit);return start
def finish(role,out,start):
 raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
