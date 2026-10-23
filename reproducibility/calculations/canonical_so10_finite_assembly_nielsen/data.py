"""FAN1 authenticated IO and exact real-radical arithmetic."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import gzip,json,os,sys,time,threading
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
L,U=s.symbols('L U',real=True);x1,x2=s.symbols('x1 x2',positive=True)
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
@lru_cache(None)
def clean(z):return s.expand(s.cancel(s.radsimp(s.expand(z))))
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def zero(M):assert not tidy(M).todok()
def dec(d):return s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']})
def enc(M):return {'shape':[int(z) for z in M.shape],'entries':[[int(i),int(j),str(z)] for (i,j),z in sorted(s.SparseMatrix(M).todok().items())]}
def nm(M):return mp.matrix([[mp.mpf(str(s.N(z,100))) for z in row] for row in M.tolist()])
def begin(prep='preparation.json'):
    start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in read(HERE/prep)['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def guard(role):
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('FAN1_PEER_RESULT_READ_DENIED')
            if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('FAN1_PHYSICAL_TARGET_READ_DENIED')
    sys.addaudithook(audit)
def save(role,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as out:out.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
def fmt(z):return mp.nstr(z,50)
FAMILIES=['VVVV','VVSS','VSS','ghostS','VVS','ghostV','VVV','SSSS','SSS']
