"""GSA1 exact ordered operators and independently resolved scalar spectrum."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
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
    a=s.Rational(v);return mp.mpf(int(a.p))/int(a.q)
def begin(prep,seconds):
    start=time.perf_counter();watch=threading.Timer(seconds,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,kind,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_{kind}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'schema':'GSA1_'+kind.upper(),'role':role,'elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
R1=load('gsa_r1_spectrum',CAL/'canonical_so10_r1_scalar_current/data.py')
number,numeric,real,tr,norm,root_value,modes_for_block=R1.number,R1.numeric,R1.real,R1.tr,R1.norm,R1.root_value,R1.modes_for_block
def input_data(role):
    gsk=load('gsa_gsk',CAL/'canonical_so10_ghost_scalar_charge_kernel/data.py')
    values,fci,scm=gsk.inputs(role);action,rho,V,ad,Ps,frame,Q,Qi,E=values
    tab=packed(CAL/'canonical_so10_ghost_scalar_charge_kernel'/f'{role}_tables.json.gz')
    units=[tuple(v) for v in tab['basis']];address={u:i for i,u in enumerate(units)}
    operators={}
    for r in range(1,5):
        for t in range(1,5):
            vv=[[parse(v) for v in row] for row in tab['operators'][f'{r},{t}']];layers=[]
            for aa,b in enumerate(frame['blocks']):
                m=b['multiplicity'];layers.append([s.SparseMatrix(m,m,{(i,j):row[address[aa,i,j]] for i in range(m) for j in range(m)}) for row in vv])
            operators[r,t]=layers
    cas=[[parse(v) for v in row] for row in tab['scalar_Casimir_averages']]
    blocks=[]
    for aa,b in enumerate(frame['blocks']):
        src=fci['blocks'][aa]
        blocks.append({'block':aa,'multiplicity':b['multiplicity'],'dimension':b['dimension'],'label':b['label'],
          'H':dec(src['H']),'projectors':[dec(src['physical']),dec(src['soft']),*map(dec,src['gold_mass_projectors'])]})
    return frame,fci,tab,operators,cas,blocks
def work_key(row,g2,lams):
    r,t=row['ghost_first'],row['ghost_second'];lammax=max(lams[r-1],lams[t-1]);lammin=min(lams[r-1],lams[t-1]);ratio=lammin/lammax
    z=mp.mpf(row['scalar_mass_base'])*(g2 if row['scalar_g2_power'] else 1)/(g2*lammax)
    return '|'.join([mp.nstr(ratio,80),mp.nstr(z,80)]),r>t,lammax
