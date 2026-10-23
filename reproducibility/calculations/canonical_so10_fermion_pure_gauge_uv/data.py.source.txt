"""GPC1 frozen IO only; no shared loop or curvature algebra."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest();packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def dec(d):return s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']})
def enc(M):return {'shape':list(M.shape),'entries':[[int(i),int(j),str(s.expand(v))] for (i,j),v in sorted(s.SparseMatrix(M).todok().items()) if v]}
def begin(role):
 start=time.perf_counter();t=threading.Timer(600,lambda:os._exit(124));t.daemon=True;t.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]))
   if p.parent.resolve()==HERE and p.name.startswith('replay' if role=='primary' else 'primary'):raise PermissionError('GPC1_PEER_DENIED')
   if p.parent.name in ['canonical_so10_split_momentum_gauge_polarization','canonical_so10_fermion_statistical_normalization']:raise PermissionError('GPC1_OLD_ANSWER_DENIED')
 sys.addaudithook(audit);return start
def finish(role,d,start):
 raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
