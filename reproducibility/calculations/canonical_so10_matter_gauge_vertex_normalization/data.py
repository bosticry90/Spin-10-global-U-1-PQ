"""MGN1 immutable IO/types only; loop and group routes remain distinct."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest();packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
LOC={name:s.Symbol(name,real=True) for rep in ['10','126'] for i in range(3) for j in range(i,3) for name in [f'u{rep}_{i}{j}',f'v{rep}_{i}{j}']}
xi,eta=s.symbols('xi eta_H')
LOC.update({'xi':xi,'eta_H':eta,'reference_width_M':xi,'reference_width_H':eta})
def dec(row):return s.SparseMatrix(*row['shape'],{(i,j):s.sympify(v,locals=LOC) for i,j,v in row['entries']})
def enc(mat):return {'shape':list(mat.shape),'entries':[[int(i),int(j),str(s.expand(v))] for (i,j),v in sorted(s.SparseMatrix(mat).todok().items()) if v]}
def begin(role):
 start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
 assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for name,hsh in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(name))==hsh,name
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   path=Path(os.fsdecode(args[0]))
   if path.parent.resolve()==HERE and path.name.startswith('replay' if role=='primary' else 'primary'):raise PermissionError('MGN1_PEER_DENIED')
 sys.addaudithook(audit);return start
def finish(role,obj,start):
 raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as handle:handle.write(blob)
 print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
