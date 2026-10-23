"""VVA1 model inputs, exact operator probes and canonical mass-role lookup."""
from pathlib import Path
from hashlib import sha256
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,enc,dec,inflate,w,QUAD
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def parse(v):return s.sympify(v,locals={'w':w})
def q(v):
    r=s.Rational(v);return mp.mpf(int(r.p))/int(r.q)
def begin(prep):
    start=time.perf_counter();watch=threading.Timer(600,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,kind,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_{kind}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'kind':kind,'elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
G=load('vva_gsa_data',CAL/'canonical_so10_ghost_scalar_sunset/data.py')
root_value,number,numeric,real,tr,norm=G.root_value,G.number,G.numeric,G.real,G.tr,G.norm
def inputs(role):
    frame,fci,old,ignored,cas,blocks=G.input_data(role)
    tab=packed(CAL/'canonical_so10_vector_vector_scalar_charge_kernel'/f'{role}_tables.json.gz')
    address={tuple(u):i for i,u in enumerate(tab['basis'])};ops={}
    for r in range(5):
        for t in range(5):
            rows=[[parse(v) for v in row] for row in tab['operators'][f'{r},{t}']];layers=[]
            for a,b in enumerate(blocks):
                m=b['multiplicity'];layers.append([s.SparseMatrix(m,m,{(i,j):row[address[a,i,j]] for i in range(m) for j in range(m)}) for row in rows])
            ops[r,t]=layers
    return frame,fci,tab,ops,cas,blocks
def work(row,g2,lams):
    r,t=row['first'],row['second'];maximum=max(lams[r],lams[t]);minimum=min(lams[r],lams[t]);assert maximum>0
    zz=mp.mpf(row['scalar_mass_base'])*(g2 if row['scalar_g2_power'] else 1)/(g2*maximum)
    if minimum==0:
        assert row['scalar_type']>=2 and abs(zz-1)<mp.mpf('1e-75');return 'light','0|1',r>t,maximum
    key=mp.nstr(minimum/maximum,80)+'|'+mp.nstr(zz,80)
    return ('soft' if row['scalar_type']==1 else 'positive'),key,r>t,maximum
def kernel_helpers():
    folder=CAL/'canonical_so10_two_vector_cubic_kernel';old=load('vva_vck_data',folder/'data.py');saved=sys.modules.get('data')
    try:
        sys.modules['data']=old;fun=load('vva_vck_functions',folder/'functions.py')
    finally:
        if saved is None:sys.modules.pop('data',None)
        else:sys.modules['data']=saved
    return old,fun
