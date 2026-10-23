"""BMC1 authenticated IO, symbols and serialization; no shared native algorithm."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
ell,g,lam1,lam2,b,c,bi,ri,W,p0,tau,alpha,a=s.symbols('ell g lambda1 lambda2 b c bi ri W C0 tau alpha a',real=True)
LOC={str(v):v for v in [ell,g,lam1,lam2,b,c,bi,ri,W,p0,tau,alpha,a]}
def read(p):return json.loads(p.read_bytes())
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def ex(v):return s.sympify(v,locals=LOC)
def begin():
    start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def guard(role):
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('BMC1_PEER_RESULT_READ_DENIED')
            if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('BMC1_PHYSICAL_DEMAND_PARSE_DENIED')
    sys.addaudithook(audit)
def save(role,out,start):
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
