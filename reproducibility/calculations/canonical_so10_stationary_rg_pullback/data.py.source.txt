"""SRG1 authenticated IO and inherited exact point arithmetic."""
from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,time,threading
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,dec,numeric,point_root,number,weights,w,xi
POWERS=[0,2,4];ALLPOWERS=[-2,0,2,4]
read=lambda p:json.loads(p.read_bytes())
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
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
            if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('SRG1_PEER_RESULT_READ_DENIED')
            if 'canonical_so10_nine_family_uv_assembly' in p.parts:raise PermissionError('SRG1_FINITE_SLOPE_READ_DENIED')
            if p.name in ['comparison_gate.json','two_loop_boundary.json','direct_matching.json']:raise PermissionError('SRG1_PHYSICAL_TARGET_READ_DENIED')
    sys.addaudithook(audit)
def enc(M):
    return {'shape':[int(z) for z in M.shape],'entries':[[int(i),int(j),str(z)] for (i,j),z in sorted(s.SparseMatrix(M).todok().items())]}
def save(role,d,start):
    raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as out:out.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
def fmt(v):
    assert abs(mp.im(v))<mp.mpf('1e-65')*(1+abs(v));return mp.nstr(mp.re(v),50)
