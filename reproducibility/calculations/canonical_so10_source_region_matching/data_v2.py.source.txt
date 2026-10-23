"""SRM1 authenticated IO only; native scientific routes are separate."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
PACKET=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def dec(d):return s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']})
def enc(M):return {'shape':list(M.shape),'entries':[[int(i),int(j),str(s.simplify(z))] for (i,j),z in sorted(s.SparseMatrix(M).todok().items()) if s.simplify(z)!=0]}
def begin(role):
    started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in read(HERE/'preparation_v2.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('SRM1_PEER_READ_DENIED')
            if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('SRM1_PHYSICAL_TARGET_DENIED')
    sys.addaudithook(audit);return started
def finish(role,out,started):
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'),default=json_integer)+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_v2_tables.json.gz')).open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role+'_v2','elapsed_after_imports':time.perf_counter()-started,'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)

def json_integer(value):
    if isinstance(value,s.Integer):return int(value)
    raise TypeError("SRM1_V2_UNSUPPORTED_JSON_TYPE:"+type(value).__name__)
