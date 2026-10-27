"""VHR1 finite spin/exterior contraction with free arbitrary-dimension color."""
from data import *
from fractions import Fraction as F
from itertools import product
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'preparation_v2.json')['input_sha256'].items():assert digest(Path(p))==h,p
def audit(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.name=='canonical_so10_ghost_vertex_order_reconciliation' and p.suffix=='.gz':raise PermissionError('VHR1_FREE_TARGET_DENIED')
sys.addaudithook(audit)
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];gm=[s.kronecker_product(pa[1],z) for z in pa]+[s.kronecker_product(pa[0],s.eye(2))];C4=gm[1]*gm[3];PL=s.diag(1,1,0,0);PR=s.eye(4)-PL
def gauss(z):
 a,b=s.expand(z).as_real_imag();assert a.is_Rational and b.is_Rational;return F(int(a.p),int(a.q)),F(int(b.p),int(b.q))
def cm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ca(a,b):return a[0]+b[0],a[1]+b[1]
def trword(w):return tuple({'G':'g','g':'G','C':'c','c':'C','R':'r','r':'R','Y':'Y','Z':'Z'}[x] for x in w[::-1])
def wedge(a,b):
 if a&b:return 0,0
 sg=(-1)**sum((b&((1<<i)-1)).bit_count() for i in range(4) if a>>i&1);return a|b,sg
def matrix_term(terms,i,j):
 z=[(gauss(m[i,j]),(word,)) for m,word in terms if m[i,j]!=0];assert len(z)<=1
 return z[0] if z else None
def factor(tag,i,j,q,extspin=None,extbit=None):
 # Return numeric coefficient,free word,exterior mask,linear-F side.
 if tag in ['BB','XX','Ca']:return ((F(1),F(0)),(),0,None)
 if tag=='aC':return ((F(-1),F(0)),(),0,None)
 if tag in ['BL','LB']:return ((F((-1 if tag=='BL' else 1)*q),F(0)),(),0,None)
 if tag=='FF':
  z=-s.I*q*(gm[0]*C4.inv())[i,j];return (gauss(z),(),0,None) if z else None
 if tag in ['GF_CaX_v','GF_XaC_v']:return ((F(-1 if tag=='GF_CaX_v' else 1),F(0)),(),2,None)
 if tag in ['GF_LX_v','GF_XL_v']:return ((F(0),F(1)),(),0,None)
 if tag in ['gC_aB','gC_Ba']:return ((F(0),F(q)),(),2,None)
 if tag in ['YP_XF','YP_FX','gP_BF','gP_FB']:
  side='col' if tag.endswith(('XF','BF')) else 'row';fs=j if side=='col' else i
  if tag.startswith('YP'):terms=[(C4*PL,'Y'),(C4*PR,'Z')]
  else:terms=[(C4*(-s.I*gm[0])*PL,'G'),(-C4*(-s.I*gm[0])*PR,'g')]
  z=matrix_term(terms,fs,extspin)
  if z is None:return None
  co,word=z
  if side=='col':co=(-co[0],-co[1])
  return co,word,extbit,side
 if tag=='M_FC_P':
  z=matrix_term([(-s.I*PL,'R'),(s.I*PR,'r')],i,extspin)
  return (z[0],z[1],1|extbit,'row') if z else None
 if tag=='M_FF_C':
  z=matrix_term([(s.I*PL,'C'),(-s.I*PR,'c')],i,j)
  return (z[0],z[1],3,None) if z else None
 if tag in ['M_BB_C','M_LL_C','M_XX_C']:return ((F(1),F(0)),(),3,None)
 if tag=='M_BC_none_d':return ((F(0),F(q)),(),1,None)
 if tag=='M_aL_none':return ((F(0),F(1)),(),1,None)
 raise AssertionError(tag)
groles={tag:(a,b) for a,b,tag in G};vroles={tag:(a,b) for a,b,tag,d in V};rroles={tag:(a,b) for a,b,tag,d in roots('primary')}
support=packed(HERE/'complete_ordered_root_support.json.gz')['words'];out=[]
for w in support:
 tags=[];roles=[]
 for path in w['path']:
  gt,vt=path.split('/');tags.extend([gt,vt]);roles.extend([groles[gt],vroles[vt]])
 tags.append(w['root']);roles.append(rroles[w['root']]);assert all(roles[i][1]==roles[(i+1)%len(roles)][0] for i in range(len(roles)))
 nodes=[a for a,b in roles];linear=[i for i,z in enumerate(tags) if z in ['YP_XF','YP_FX','gP_BF','gP_FB','M_FC_P']];assert len(linear)==2
 kernels=[[defaultdict(lambda:(F(0),F(0))) for j in range(4)] for i in range(4)]
 for spins in product(*[range(4) if x=='F' else range(1) for x in nodes]):
  for q in [-1,1]:
   for su,sv in product(range(4),repeat=2):
    for assignment in [(4,8),(8,4)]:
     factors=[];mask=0;co=(F(w['sign']*(-1 if nodes[0] in ['F','a','C'] else 1)),F(0));ok=True
     for i,tag in enumerate(tags):
      if i in linear:
       bit=assignment[linear.index(i)];sp=su if bit==4 else sv
      else:bit=sp=None
      # G uses row momentum q; the following V uses its row momentum -q.
      qq=q if i==len(tags)-1 or i%2==0 else -q
      z=factor(tag,spins[i],spins[(i+1)%len(tags)],qq,sp,bit)
      if z is None or z[0]==(0,0):ok=False;break
      mask,sg=wedge(mask,z[2])
      if not sg:ok=False;break
      co=cm(co,z[0]);co=(sg*co[0],sg*co[1]);factors.append(z)
     if not ok:continue
     assert mask==15
     col=next(i for i,z in enumerate(factors) if z[3]=='col');row=next(i for i,z in enumerate(factors) if z[3]=='row');word=trword(factors[col][1]);i=(col+1)%len(tags)
     while i!=row:
      assert nodes[i]=='F' and factors[i][3] is None;word+=factors[i][1];i=(i+1)%len(tags)
     word+=factors[row][1]
     if factors[col][2]&8:word=trword(word)
     kernels[su][sv][word]=ca(kernels[su][sv][word],(co[0]/2,co[1]/2))
 serial=[]
 for i in range(4):
  for j in range(4):
   for word,(a,b) in sorted(kernels[i][j].items()):
    if a or b:serial.append([i,j,list(word),str(a),str(b)])
 out.append({'word':w,'free_spin_kernel':serial})
 print('STAGE FREE_SPIN_COLOR_WORD',w['n'],w['root'],len(serial),flush=True)
result={'method':'arbitrary_dimension_open_color_index_line_four_spin_and_exterior_paths','words':out,'normalization':'PAIRED_MODES_SUPERTRACE_GAUSSIAN_HALF','color_dimension':'ARBITRARY_FREE_NONCOMMUTATIVE_WORDS','quantum_target_read':False,'elapsed_after_imports':time.perf_counter()-t}
raw=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'free_words_v2_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':result['elapsed_after_imports']},sort_keys=True),flush=True)
