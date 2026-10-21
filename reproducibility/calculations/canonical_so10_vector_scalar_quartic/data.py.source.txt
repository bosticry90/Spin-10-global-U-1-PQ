"""VSP1 IO, inherited exact field and physical representations."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import gzip,json,sys,time,os,threading
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,dec,enc,weights,point_root,number,numeric,tr,real,fmt,w,QUAD
def read(p):return json.loads(p.read_bytes())
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
def save(role,kind,tab,start,extra=None):
    raw=(json.dumps(tab,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    p=HERE/(role+'_'+kind+'_tables.json.gz')
    with p.open('xb') as out:out.write(blob)
    result={'schema':'VSP1_'+kind.upper(),'role':role,'elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),
      'raw_bytes':len(raw),'packed_bytes':len(blob)}
    if extra:result.update(extra)
    print('RESULT '+json.dumps(result,sort_keys=True),flush=True)
def begin(prep='preparation.json'):
    start=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for n,h in read(HERE/prep)['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    return start
def inputs(role):
    d=read(PK/('frozen_a10_physical_reconciliation/full_'+role+'.json'))
    reps=d['representation_matrices'];rho=[]
    for a in range(45):rho.append(s.SparseMatrix(s.diag(*[dec(reps[k][a]) for k in ['Phi','Sigma','phi','S']])))
    f=packed(CAL/'canonical_so10_background_threshold_inputs'/f'{role}_tables.json.gz')['f']
    V=dec(packed(CAL/'canonical_so10_vector_quartic_ir_matching'/f'{role}_tables.json.gz')['light_embedding'])
    ad=[]
    for h in range(12):
        E=s.SparseMatrix(45,45,{})
        for a,b,c,z in f:
            if V[a,h]:E[c,b]+=V[a,h]*s.sympify(z)
        ad.append(tidy(E))
    Ps=list(map(dec,packed(CAL/'canonical_so10_width_hard_projection'/f'{role}_tables.json.gz')['projectors']))
    frame=packed(CAL/'canonical_so10_scalar_sm_frame'/f'{role}_tables.json.gz')
    Q,D=dec(frame['Q']),dec(frame['D']);Qi=s.SparseMatrix(328,328,{(i,i):1/D[i,i] for i in range(328)})*Q.H
    seeds=[b['offset']+j for b in frame['blocks'] for j in range(b['multiplicity'])]
    E=Q[:,seeds];zero(E.H*E-s.eye(65))
    return d,rho,V,ad,Ps,frame,Q,Qi,E
def inflate(blocks,small):
    out={}
    for b,M in zip(blocks,small):
        m=b['multiplicity'];off=b['offset']
        for k in range(b['dimension']):
            for (i,j),z in M.todok().items():out[off+k*m+i,off+k*m+j]=z
    return s.SparseMatrix(328,328,out)
