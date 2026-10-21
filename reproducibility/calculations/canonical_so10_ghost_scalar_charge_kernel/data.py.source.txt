"""GSK1 frozen exact inputs and signed operator helpers."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,enc,dec,inflate,weights,w,QUAD
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def begin(prep,seconds):
    start=time.perf_counter();watch=threading.Timer(seconds,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'schema':'GSK1_NATIVE','role':role,'elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def inputs(role):
    vsp=load('gsk_vsp',CAL/'canonical_so10_vector_scalar_quartic/data.py')
    values=vsp.inputs(role)
    fci=packed(CAL/'canonical_so10_finite_counterterm_insertion'/f'{role}_v3_tables.json.gz')
    scm=packed(CAL/'canonical_so10_scalar_current_sm_kernel'/f'{role}_tables.json.gz')
    return values,fci,scm
def basis(frame):return [(a,i,j) for a,b in enumerate(frame['blocks']) for i in range(b['multiplicity']) for j in range(b['multiplicity'])]
def action_tensor(action,rho):
    O=dec(action['vacuum']['orbit']);B=[O.T*R for R in rho]
    return s.SparseMatrix(2025,328,{(a*45+b,i):v for b,M in enumerate(B) for (a,i),v in M.todok().items()})
def tensor_table():
    tab=packed(CAL/'canonical_so10_background_threshold_inputs/primary_tables.json.gz')
    return s.SparseMatrix(2025,328,{(a*45+b,i):s.sympify(v) for a,b,i,v in tab['T']})
def Xcolumns(M):
    grouped=[{} for _ in range(M.cols)]
    for (ab,col),v in M.todok().items():grouped[col][divmod(ab,45)]=v
    return [s.SparseMatrix(45,45,g) for g in grouped]
def trace_pair(A,B):return sum((v*B[j,i] for (i,j),v in A.todok().items()),s.S.Zero)
def shapes(C,X,Y):
    # X=conjugate(T_rs) and Y=conjugate(T_sr); scalar conjugation only.
    Cr,Cs=C
    return [(X/2,Y/2),*[(Cr[i]*X/2,Y*Cr[i]/2) for i in range(3)],*[(X*Cs[i]/2,Cs[i]*Y/2) for i in range(3)]]
def coefficient(forms,back,forward):return [trace_pair(L,back)+trace_pair(R,forward) for L,R in forms]
def pairing(vec,proj,frame,B,cas=None):
    return red(sum((frame['blocks'][a]['dimension']*v*proj[a][j,i]*(1 if cas is None else cas[a]) for v,(a,i,j) in zip(vec,B)),s.S.Zero))
def small_types(fci):
    rows=fci['blocks'];return [[dec(b['physical']) for b in rows],[dec(b['soft']) for b in rows]]+[[dec(b['gold_mass_projectors'][r]) for b in rows] for r in range(4)]
def probes(operators,frame,B,cas,fci):
    types=small_types(fci);out=[]
    for r in range(5):
        for t in range(5):
            ops=operators[f'{r},{t}']
            for typ,P in enumerate(types):
                out.append({'first_ghost':r,'second_ghost':t,'scalar_type':typ,
                  'raw':str(pairing(ops[0],P,frame,B)),
                  'q1_squared':[str(pairing(ops[1+i],P,frame,B)) for i in range(3)],
                  'q2_squared':[str(pairing(ops[4+i],P,frame,B)) for i in range(3)],
                  'qscalar_squared':[str(pairing(ops[0],P,frame,B,[c[i] for c in cas])) for i in range(3)]})
    return out
