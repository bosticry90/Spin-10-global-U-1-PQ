"""HPR1 fixed evidence IO and symbolic/numeric types."""
from pathlib import Path
from hashlib import sha256
import json,gzip,sys,time,threading,os
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
e,j,L,lg,rho,delta,q=s.symbols('eps j L lg rho delta q',real=True)
LOC={str(v):v for v in [e,j,L,lg,rho,delta,q]}
def ex(v):return s.sympify(v,locals=LOC)
def clean(v):return s.factor(s.cancel(s.sympify(v)))
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def begin(prep='preparation.json'):
    start=time.perf_counter();t=threading.Timer(600,lambda:os._exit(124));t.daemon=True;t.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def guard(role):
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('HPR1_PEER_TARGET_READ_DENIED')
            if p.name=='comparison_gate.json':raise PermissionError('HPR1_PHYSICAL_TARGET_READ_DENIED')
    sys.addaudithook(audit)
def save(role,out,start):
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def strs(v):return list(map(str,v))
def fmt(v):return mp.nstr(v,35)
