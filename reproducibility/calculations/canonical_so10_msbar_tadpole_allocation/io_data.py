"""MTA1 authenticated IO and serialization only; no shared native mathematics."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CAL=ROOT/'calculations';HTB=CAL/'canonical_so10_heavy_tadpole_bridge'
KEYS=['constant','scale_log','coupling_log'];POWERS=[-2,0,2,4]
def read(p):return json.loads(p.read_bytes())
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def begin(prep='preparation.json'):
    started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in read(HERE/prep)['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return started
def guard(role):
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('MTA1_PEER_OUTPUT_READ_DENIED')
            if p.name=='comparison_gate.json':raise PermissionError('MTA1_PHYSICAL_TARGET_READ_DENIED')
    sys.addaudithook(audit)
def dec(d):return s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z) for i,j,z in d['entries']})
def clean(z):return s.factor(s.cancel(s.sympify(z)))
def num(A):return mp.matrix([[mp.mpf(str(s.N(z,100))) for z in row] for row in A.tolist()])
def rows(A):return [[mp.nstr(A[i,j],60) for j in range(A.cols)] for i in range(A.rows)]
def vector(A):return [mp.nstr(z,60) for z in A]
def save(role,d,started):
    raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as out:out.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-started,'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
