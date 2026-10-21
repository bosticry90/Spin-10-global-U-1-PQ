"""VSSA1 exact-frame input and high-precision spectral helpers."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,enc,dec,inflate,w,QUAD
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def begin(prep,seconds):
    start=time.perf_counter();watch=threading.Timer(seconds,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for name,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(name).read_bytes()).hexdigest()==h,name
    return start
def save(role,kind,value,start):
    raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_{kind}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'schema':'VSSA1_'+kind.upper(),'role':role,'elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def root_value(role):
    aa,bb,cc=[mp.mpf(str(s.N(v,125))) for v in QUAD]
    return (-bb+mp.sqrt(bb*bb-4*aa*cc))/(2*aa) if role=='primary' else -2*cc/(bb+mp.sqrt(bb*bb-4*aa*cc))
@lru_cache(10000)
def number(v,root):
    re,im=s.expand(red(v)).as_real_imag();env={w:s.Float(mp.nstr(root,120),120)}
    return mp.mpc(str(s.N(re.subs(env),120)),str(s.N(im.subs(env),120)))
def numeric(M,root):return mp.matrix([[number(M[i,j],root) for j in range(M.cols)] for i in range(M.rows)])
def real(v):
    assert abs(mp.im(v))<mp.mpf('1e-85')*(1+abs(v)),str(v)
    return mp.re(v)
def tr(M):return sum((M[i,i] for i in range(M.rows)),mp.mpf(0))
def norm(M):return max([abs(v) for v in M] or [mp.mpf(0)])
