"""VHR1 independent literal paired-mode sparse exterior supertraces."""
from data import *
import importlib.util
from itertools import combinations
from fractions import Fraction as F
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'preparation_v2.json')['input_sha256'].items():assert digest(Path(p))==h,p
spec=importlib.util.spec_from_file_location('vhr_hwb_exact',CAL/'canonical_so10_tangent_heat_ward_bridge/data.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
def audit(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==HERE and p.name.startswith('free_words_v2'):raise PermissionError('VHR1_FREE_PEER_DENIED')
  if p.parent.name=='canonical_so10_ghost_vertex_order_reconciliation' and p.suffix=='.gz':raise PermissionError('VHR1_PAIR_TARGET_DENIED')
sys.addaudithook(audit)
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];gam=[s.kronecker_product(pa[1],z) for z in pa]+[s.kronecker_product(pa[0],s.eye(2))];C4=gam[1]*gam[3];PL=s.diag(1,1,0,0);PR=s.eye(4)-PL
cases=[(s.Matrix([[1,1+s.I],[1-s.I,-2]]),s.Matrix([[2,-s.I],[s.I,-1]]),s.Matrix([[-1,2-s.I],[2+s.I,3]]),s.Matrix([[1+s.I,2-s.I],[2-s.I,-1+2*s.I]])),(s.Matrix([[2,-s.I],[s.I,-1]]),s.Matrix([[0,1+2*s.I],[1-2*s.I,2]]),s.Matrix([[3,-2+s.I],[-2-s.I,1]]),s.Matrix([[2,-1+s.I],[-1+s.I,3-s.I]]))]
support=packed(HERE/'complete_ordered_root_support.json.gz')['words'];outputs=[];ordinary_changed=0
groles={tag:(a,b) for a,b,tag in G}
def kind(i):return ['B','L','X','C','a'][i%13] if i%13<5 else 'F'
def serialize(m):
 return {'shape':list(m.shape),'entries':[[i,j,str(s.expand(z))] for (i,j),z in sorted(s.SparseMatrix(m).todok().items()) if z]}
for ci,(TG,TC,TR,Y) in enumerate(cases):
 cc=s.kronecker_product(C4,s.eye(2));gamma=s.kronecker_product(gam[0],s.eye(2));ag=s.kronecker_product(PL,TG)-s.kronecker_product(PR,TG.T);ac=s.kronecker_product(PL,TC)-s.kronecker_product(PR,TC.T);ar=s.kronecker_product(PL,TR)-s.kronecker_product(PR,TR.T);yy=cc*(s.kronecker_product(PL,Y)+s.kronecker_product(PR,s.conjugate(Y)));fb=cc*(-s.I*gamma*ag);ff=-s.I*gamma*cc.inv();par=([0,0,0]+[1]*10)*2;at=lambda mode,i:mode*13+i
 gm={}
 for mode,q in enumerate([-1,1]):
  other=1-mode
  for a,b,z in [(0,0,3),(0,1,-q),(1,0,q),(2,2,1),(3,4,1),(4,3,-1)]:gm[at(mode,a),at(other,b)]=e.ex(0,z)
  for i in range(8):
   for j in range(8):
    if ff[i,j]:gm[at(mode,5+i),at(other,5+j)]=e.ex(0,q*ff[i,j])
 gtables={tag:{ij:z for ij,z in gm.items() if (kind(ij[0]),kind(ij[1]))==roles} for tag,roles in groles.items()}
 kernels=[s.zeros(8) for w in support]
 for aa,bb in combinations(range(8),2):
  pp=[{} for _ in range(8)];pp[aa]=e.ex(4,1);pp[bb]=e.ex(8,1)
  def lin(m,i):return e.add(*(e.mul(e.ex(0,m[i,j]),pp[j]) for j in range(8) if m[i,j]))
  vt={tag:{} for a,b,tag,d in V};mt={tag:{} for a,b,tag,d in roots('replay')}
  for mode,q in enumerate([-1,1]):
   other=1-mode
   vt['GF_CaX_v'][at(mode,4),at(other,2)]=e.ex(2,-1);vt['GF_XaC_v'][at(mode,2),at(other,4)]=e.ex(2,1)
   vt['GF_LX_v'][at(mode,1),at(other,2)]=e.ex(0,s.I);vt['GF_XL_v'][at(mode,2),at(other,1)]=e.ex(0,s.I)
   vt['gC_aB'][at(mode,4),at(other,0)]=e.ex(2,s.I*q);vt['gC_Ba'][at(mode,0),at(other,4)]=e.ex(2,s.I*q)
   for tag,node in [('M_BB_C',0),('M_LL_C',1),('M_XX_C',2)]:mt[tag][at(mode,node),at(mode,node)]=e.ex(3,1)
   mt['M_BC_none_d'][at(mode,0),at(mode,3)]=e.ex(1,s.I*q);mt['M_aL_none'][at(mode,4),at(mode,1)]=e.ex(1,s.I)
   for i in range(8):
    fy,fg=lin(yy,i),lin(fb,i)
    if fy:vt['YP_XF'][at(mode,2),at(other,5+i)]=e.scale(fy,-1);vt['YP_FX'][at(mode,5+i),at(other,2)]=fy
    if fg:vt['gP_BF'][at(mode,0),at(other,5+i)]=e.scale(fg,-1);vt['gP_FB'][at(mode,5+i),at(other,0)]=fg
    root=e.mul(e.ex(1,-s.I),lin(ar,i))
    if root:mt['M_FC_P'][at(mode,5+i),at(mode,3)]=root
    for j in range(8):
     if ac[i,j]:mt['M_FF_C'][at(mode,5+i),at(mode,5+j)]=e.ex(3,s.I*ac[i,j])
  xcache={}
  for wi,w in enumerate(support):
   seq=[]
   for path in w['path']:
    if path not in xcache:
     gt,tag=path.split('/');xcache[path]=e.mm(gtables[gt],vt[tag])
    seq.append(xcache[path])
   val=seq[0]
   for x in seq[1:]:val=e.mm(val,x)
   val=e.ms(e.mm(val,mt[w['root']]),w['sign']);tr=e.trace(val,par).get(15,(0,0));z=s.Rational(tr[0],2)+s.I*s.Rational(tr[1],2);kernels[wi][aa,bb]=z;kernels[wi][bb,aa]=-z
   ordinary_changed+=int(e.trace(val,par,True)!=e.trace(val,par))
 outputs.append({'case':ci,'G':serialize(TG),'C':serialize(TC),'R':serialize(TR),'Y':serialize(Y),'kernels':[serialize(k) for k in kernels]})
 print('STAGE PAIRED_MODE_ALL_WORDS',ci,len(support),flush=True)
result={'method':'literal_sparse_paired_mode_matrix_products_integer_exterior_and_supertrace','cases':outputs,'ordinary_trace_changed_word_pairs':ordinary_changed,'external_pairs_per_case':28,'word_count':len(support),'quantum_target_read':False,'elapsed_after_imports':time.perf_counter()-t}
raw=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'paired_words_v2_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':result['elapsed_after_imports']},sort_keys=True),flush=True)
