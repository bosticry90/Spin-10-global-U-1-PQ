from pathlib import Path
from hashlib import sha256
from collections import defaultdict
from functools import lru_cache
import gzip,json,sys,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];assert role in ['primary','replay']
for p,h in read(O/'endpoint_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==O and p.name.startswith('endpoint_'+('replay' if role=='primary' else'primary')):raise PermissionError('HP1_PEER_DENIED')
sys.addaudithook(guard)
g,xi,eta=s.symbols('g10 xi eta_H',real=True);loc={'g10':g,'xi':xi,'eta_H':eta}
@lru_cache(None)
def parse(z):return s.sympify(z,locals=loc)
dec=lambda d:s.SparseMatrix(*d['shape'],{(i,j):parse(z) for i,j,z in d['entries']});tidy=lambda M:s.SparseMatrix(M).applyfunc(s.expand)
def enc(M):return {'shape':list(M.shape),'entries':[[i,j,str(s.expand(v))] for (i,j),v in sorted(s.SparseMatrix(M).todok().items()) if s.expand(v)!=0]}
def mm(A,B):
 if role=='primary':return tidy(A*B)
 rows=defaultdict(list);out=defaultdict(list)
 for (k,j),v in B.todok().items():rows[k].append((j,v))
 for (i,k),v in A.todok().items():
  for j,z in rows[k]:out[i,j].append(v*z)
 return tidy(s.SparseMatrix(A.rows,B.cols,{k:s.Add(*v) for k,v in out.items()}))
d=json.loads(gzip.decompress((O/('endpoint_'+role+'_inputs.json.gz')).read_bytes()));G0=dec(d['G0']);N0=dec(d['N0']);W=s.diag(*([eta]*12+[xi]*33));S=s.diag(*([-1]*45+[1]*45));Gr=[dec(z['Gr']) for z in d['probe_quadratics']];U=[dec(z['U']) for z in d['probe_quadratics']];Nr=[dec(z['Nr']) for z in d['probe_quadratics']];Jrho=[dec(z['J']) for z in d['rho']];Ju=[[dec(z['Ju']) for z in row] for row in d['mixed']];J0=list(map(dec,d['J0']));currents=[('rho'+str(r),Jrho[r]) for r in range(2)]+[('u'+str(r)+'_C'+str(c),Ju[r][c]) for r in range(2) for c in range(45)]
polarization=[];nulls=[];scalar_nulls=[];controls={'omit_auxiliary_current_null_positions':0,'wrong_right_momentum_sign_isotropy_positions':0}
for label,J in currents:
 pol=tidy(J[:,45:]+mm(J[:,:45],W)/2);polarization.append([label,enc(pol)]);jg=mm(J,G0);bad=s.SparseMatrix(J)
 for(i,j),v in list(bad.todok().items()):
  if j>=45:bad[i,j]=0
 for r in range(2):
  nulls.append([label,r,enc(mm(J,Gr[r]))]);scalar_nulls.append([label,r,enc(mm(jg,Nr[r]))]);controls['omit_auxiliary_current_null_positions']+=len(mm(bad,Gr[r]).todok())
 controls['wrong_right_momentum_sign_isotropy_positions']+=len(mm(jg,J.T).todok())
U_products=[[r,t,enc(mm(mm(U[r],G0),U[t]))] for r in range(2) for t in range(2)];G_N_products=[[r,t,enc(mm(Gr[r],Nr[t]))] for r in range(2) for t in range(2)];column_polarization=[enc(tidy(Nr[r][45:,:]-mm(W,Nr[r][:45,:])/2)) for r in range(2)]
degrees=[(0,0),(1,0),(0,1)];GG=[G0,*Gr];NN=[N0,*Nr]
def plus(*powers):return tuple(sum(z[i] for z in powers) for i in range(2))
def assemble(events,shape):return {str(k[0])+','+str(k[1]):enc(tidy(sum(v,s.zeros(*shape)))) for k,v in sorted(events.items())}
endpoint_higher=[];scalar_higher=[];rho_higher=[]
GN={(b,c):mm(GG[b],NN[c]) for b in range(3) for c in range(3)} if role=='replay' else None
for c in range(45):
 JJ=[J0[c],Ju[0][c],Ju[1][c]];jg={(a,b):mm(JJ[a],GG[b]) for a in range(3) for b in range(3)} if role=='primary' else None;ep=defaultdict(list);sp=defaultdict(list)
 for a in range(3):
  for b in range(3):
   mon=plus(degrees[a],degrees[b])
   if sum(mon)>=2:ep[mon].append(jg[a,b] if role=='primary' else mm(JJ[a],GG[b]))
   for z in range(3):
    mon=plus(degrees[a],degrees[b],degrees[z])
    if sum(mon)>=2:sp[mon].append(-mm(jg[a,b],NN[z]) if role=='primary' else -mm(JJ[a],GN[b,z]))
 endpoint_higher.append(assemble(ep,(45,90)));scalar_higher.append(assemble(sp,(45,328)))
for r in range(2):
 ep=defaultdict(list)
 for b in range(3):
  for c in range(3):
   mon=plus(degrees[b],degrees[c])
   if sum(mon)>=1:ep[mon].append(-mm(mm(Jrho[r],GG[b]),NN[c]) if role=='primary' else-mm(Jrho[r],GN[b,c]))
 rho_higher.append(assemble(ep,(45,328)))
# A dimension-independent free-word proof keeps V,W,Z noncommuting.
V,WW,Z=s.symbols('V W Z',commutative=False);left=s.Matrix([[-s.I*V,s.I*V*WW/2]]);freeG=s.Matrix([[WW,-1],[1,0]]);right=s.Matrix([[s.I*Z],[s.I*WW*Z/2]]);generic=s.expand((left*freeG*right)[0]);wrong=s.expand((left*freeG*s.Matrix([[-s.I*Z],[s.I*WW*Z/2]]))[0]);assert generic==0 and wrong!=0
out={'schema':'HIGHER_PROBE_ENDPOINT_ALGEBRA_V1','role':role,'current_polarization_remainders':polarization,'probe_current_inverse_products':nulls,'probe_current_free_inverse_scalar_products':scalar_nulls,'mixed_U_G0_U_products':U_products,'inverse_scalar_products':G_N_products,'scalar_column_polarization_remainders':column_polarization,'endpoint_degree2_coefficients_all45C':endpoint_higher,'intrinsic_scalar_degree2_and3_coefficients_all45C':scalar_higher,'rho_u_scalar_coefficients':rho_higher,'generic_noncommuting_opposite_momentum_isotropy':str(generic),'generic_wrong_right_momentum_isotropy':str(wrong),'controls':controls,'new_quantum_loop_coefficient_measured':False,'full_QAP_or_authority_changed':False}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with(O/('endpoint_'+role+'_tables.json.gz')).open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'elapsed_after_imports':time.perf_counter()-tick,'packed_sha256':sha256(blob).hexdigest(),'raw_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
