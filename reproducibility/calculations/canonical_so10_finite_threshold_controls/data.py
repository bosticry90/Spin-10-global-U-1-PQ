"""FCT1 authenticated IO and number conversion only."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes())
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def begin(role):
    start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    peer='replay' if role=='primary' else 'primary'
    def audit(event,args):
        if event=='open' and args and isinstance(args[0],(str,bytes)):
            p=Path(os.fsdecode(args[0]))
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('FCT1_PEER_DENIED')
            if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('FCT1_TARGET_DENIED')
    sys.addaudithook(audit);return start
def dec(d):return s.SparseMatrix(*d['shape'],{(int(i),int(j)):s.sympify(z,locals={'w':w}) for i,j,z in d['entries']})
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,w,QUAD
def root_value():
    a,b,c=[mp.mpf(str(s.N(v,mp.mp.dps+8))) for v in QUAD];return -2*c/(b+mp.sqrt(b*b-4*a*c))
def num(z):
    z=s.sympify(z,locals={'w':w});v=z.subs(w,s.Float(mp.nstr(root_value(),mp.mp.dps+5),mp.mp.dps+5))
    a,b=s.expand_complex(v).as_real_imag();return mp.mpc(str(s.N(a,mp.mp.dps)),str(s.N(b,mp.mp.dps)))
def mat(M):return mp.matrix([[num(z) for z in row] for row in M.tolist()])
def fmt(z):
    assert abs(mp.im(z))<mp.mpf('1e-65')*(1+abs(z));return mp.nstr(mp.re(z),65)
def finish(role,out,start):
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
