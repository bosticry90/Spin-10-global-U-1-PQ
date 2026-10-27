from data import *
from fractions import Fraction as F
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation_v2.json')['input_sha256'].items():assert digest(Path(p))==h,p
P=packed(HERE/'free_words_v2_tables.json.gz');R=packed(HERE/'paired_words_v2_tables.json.gz');support=packed(HERE/'complete_ordered_root_support.json.gz')['words'];assert P['method']!=R['method'] and [x['word'] for x in P['words']]==support
def dec(m):return s.SparseMatrix(*m['shape'],{(i,j):s.sympify(z) for i,j,z in m['entries']})
def addpoly(a,b):
 out=dict(a)
 for k,z in b.items():out[k]=s.expand(out.get(k,0)+z)
 return {k:z for k,z in out.items() if z!=0}
def scale(a,c):return {k:s.expand(z*c) for k,z in a.items() if s.expand(z*c)!=0}
def trword(w):return tuple({'G':'g','g':'G','C':'c','c':'C','R':'r','r':'R','Y':'Y','Z':'Z'}[x] for x in w[::-1])
def poly(row):return {tuple(w):s.Rational(a)+s.I*s.Rational(b) for w,a,b in row}
kernels=[]
for record in P['words']:
 kernel=[[{} for j in range(4)] for i in range(4)]
 for i,j,w,a,b in record['free_spin_kernel']:kernel[i][j]=addpoly(kernel[i][j],{tuple(w):s.Rational(a)+s.I*s.Rational(b)})
 for i in range(4):
  for j in range(4):assert not addpoly(kernel[i][j],{trword(w):z for w,z in kernel[j][i].items()}),'ALTERNATING_FREE_KERNEL'
 kernels.append(kernel)
positions=0
for case in R['cases']:
 gen={key:dec(case[key]) for key in ['G','C','R','Y']};gen.update({'g':gen['G'].T,'c':gen['C'].T,'r':gen['R'].T,'Z':s.conjugate(gen['Y'])})
 for wi,kernel in enumerate(kernels):
  m=s.zeros(8)
  for i in range(4):
   for j in range(4):
    block=s.zeros(2)
    for word,z in kernel[i][j].items():
     prod=s.eye(2)
     for token in word:prod=prod*gen[token]
     block+=z*prod
    m[2*i:2*i+2,2*j:2*j+2]=block
  delta=(m-dec(case['kernels'][wi])).applyfunc(s.simplify);assert not delta.todok(),(case['case'],wi,delta);positions+=64
assert R['ordinary_trace_changed_word_pairs']>0
pair_proofs={}
for n in [3,4]:
 ids=[i for i,w in enumerate(support) if w['n']==n and w['root'] in ['M_BC_none_d','M_aL_none']];assert len(ids)==2
 for i in range(4):
  for j in range(4):assert not addpoly(kernels[ids[0]][i][j],kernels[ids[1]][i][j]),('NONZERO_CONSTANT_ROOT_PAIR',n,i,j)
 pair_proofs[str(n)]={'word_indices':ids,'universal_free_polynomial_remainder':0,'individual_word_nonzero':all(any(kernels[z][i][j] for i in range(4) for j in range(4)) for z in ids)}
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];gam=[s.kronecker_product(pa[1],z) for z in pa]+[s.kronecker_product(pa[0],s.eye(2))];C4=gam[1]*gam[3];PL=s.diag(1,1,0,0);PR=s.eye(4)-PL;HL,HR=C4*PL,C4*PR
li,lj=next((i,j) for i in range(4) for j in range(4) if HL[i,j]);ri,rj=next((i,j) for i in range(4) for j in range(4) if HR[i,j]);templates=[]
def serialized(p):return [[list(w),str(s.re(z)),str(s.im(z))] for w,z in sorted(p.items())]
for wi,(kernel,w) in enumerate(zip(kernels,support)):
 holo=scale(kernel[li][lj],1/HL[li,lj]);anti=scale(kernel[ri][rj],1/HR[ri,rj])
 for i in range(4):
  for j in range(4):assert not addpoly(kernel[i][j],scale(addpoly(scale(holo,HL[i,j]),scale(anti,HR[i,j])),-1)),('PROJECTOR_RECONSTRUCTION',wi,i,j)
 assert not addpoly(holo,{trword(k):-z for k,z in holo.items()});assert not addpoly(anti,{trword(k):-z for k,z in anti.items()})
 templates.append({'word':w,'holo':serialized(holo),'anti':serialized(anti),'free_spin_kernel':P['words'][wi]['free_spin_kernel']})
artifact={'schema':'VHR1_UNIVERSAL_ORDERED_WORD_COEFFICIENTS','templates':templates,'constant_root_pair_proofs':pair_proofs,'color_universality':'EXPLICIT_OPEN_COLOR_INDEX_CONTRACTION_WITH_FREE_NONCOMMUTATIVE_WORDS','actual_Spin10_n3_sum_calculated':False,'complete_regulated_identity_qualified':False,'scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps(artifact,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'universal_word_coefficients_v2.json.gz').open('xb') as f:f.write(blob)
out={'status':'QUALIFIED_UNIVERSAL_HEAT_WORD_SPIN_COLOR_TEMPLATES_AND_CONSTANT_ROOT_PAIRS','numeric_witness_matrix_positions':positions,'exact_noncommuting_cases':len(R['cases']),'word_count':len(support),'constant_root_pair_proofs':pair_proofs,'ordinary_trace_changed_word_pairs':R['ordinary_trace_changed_word_pairs'],'actual_Spin10_n3_sum_calculated':False,'complete_regulated_identity_qualified':False,'physical_scheme_adopted':False,'authority':'34/39','scientific_acceptance':'NOT_PERFORMED','artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':time.perf_counter()-t}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
