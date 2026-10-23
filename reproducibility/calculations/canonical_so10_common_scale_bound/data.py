"""CSB1 exact rational IO and scoped resource/peer controls."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import gzip,json,os,sys,threading,time
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes())
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
TAU_LO=768*F(3)**4;TAU_HI=768*F(22,7)**4
def q(v):
 v=F(str(v));return mp.mpf(v.numerator)/v.denominator
fmt=lambda v:mp.nstr(v,65)
def begin(role):
 start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
 assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]))
   if p.parent.resolve()==HERE and p.name.startswith('replay' if role=='primary' else 'primary'):raise PermissionError('CSB1_PEER_DENIED')
   if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('CSB1_TARGET_DENIED')
 sys.addaudithook(audit);return start
def finish(role,out,start):
 raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
