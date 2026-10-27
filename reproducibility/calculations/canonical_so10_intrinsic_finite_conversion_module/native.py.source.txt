from pathlib import Path
from hashlib import sha256
from collections import defaultdict
import json,gzip,sys,time,threading,os,itertools,math,sympy as s
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));H=lambda p:sha256(p.read_bytes()).hexdigest();tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];assert role in ['primary','replay']
for p,h in read(O/'preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==O and p.name.startswith('replay' if role=='primary' else'primary'):raise PermissionError('IFC_PEER_DENIED')
  if p.parent.name in ['canonical_so10_intrinsic_ghost_root_schur','canonical_so10_intrinsic_regulator_root_v2']:raise PermissionError('IFC_LATE_MASS_ROOT_DENIED')
sys.addaudithook(guard)
g,xi,eta=s.symbols('g10 xi eta_H',real=True);loc={'g10':g,'xi':xi,'eta_H':eta};dec=lambda z:s.SparseMatrix(*z['shape'],{(i,j):s.sympify(v,locals=loc) for i,j,v in z['entries']});cl=lambda M:s.SparseMatrix(M).applyfunc(s.expand);enc=lambda M:{'shape':list(M.shape),'entries':[[int(i),int(j),str(v)] for(i,j),v in sorted(cl(M).todok().items()) if v]};d=load(O/(role+'_inputs.json.gz'));zero=lambda:s.SparseMatrix(328,1,{})
# Full type enumeration in half-dimension units, including a formal derivative.
types={'B':(2,0,0,1),'x':(2,0,0,0),'C':(2,1,1,0),'a':(2,-1,1,0),'L':(4,0,0,0),'P':(3,0,1,2),'JB':(4,-1,1,1),'Jx':(4,-1,1,0),'JC':(4,-2,0,0),'Ja':(4,0,0,0),'JL':(2,-1,1,0),'KP':(3,-1,0,2),'derivative':(2,0,0,1)}
envelope=[];allowed=[];names=list(types)
for probe,dim,gh,par in [('u',0,0,0),('rho',2,1,1)]:
 for n in range(1,4):
  for ww in itertools.combinations_with_replacement(names,n):
   if not any(z.startswith('J') or z=='KP' for z in ww):continue
   if dim+2+sum(types[z][0] for z in ww)!=8 or gh+sum(types[z][1] for z in ww)!=0 or (par+sum(types[z][2] for z in ww))%2:continue
   entry=[probe,list(ww)];envelope.append(entry)
   # In this small envelope there are no paired spinor indices or even positive vector rank.
   if sum(types[z][3] for z in ww)==0:allowed.append(entry)
assert sorted([ww for probe,ww in allowed if 'Jx' in ww])==[['C','Jx'],['Jx']]
# Qx is reconstructed from its actual density, before source restriction.
xs=d['xs'];xid={n:i for i,n in enumerate(xs)};frame=d['frame'];order=frame['field_order'];phys=[f'B{i}_{mu}' for i in range(45) for mu in range(4)]+xs+[('b' if i<12 else'L')+str(i) for i in range(45)]+['C'+str(i) for i in range(45)]+[('bar' if i<12 else'ub')+str(i) for i in range(45)];ri={n:i for i,n in enumerate(order)};pi={n:i for i,n in enumerate(phys)};TI=dec(frame['physical_to_raw_inverse']);TF=dec(frame['physical_to_raw_kernel']);cs=['C'+str(i) for i in range(45)];Tc=TI.extract([ri[z] for z in cs],[pi[z] for z in cs]);Fc=TF.extract([pi[z] for z in cs],[ri[z] for z in cs]);Tx=TI.extract([ri[z] for z in xs],[pi[z] for z in xs]);Fx=TF.extract([pi[z] for z in xs],[ri[z] for z in xs]);assert not cl(Fc*Tc-s.eye(45)).todok() and not cl(Fx*Tx-s.eye(328)).todok()
Rraw=[s.SparseMatrix(328,328,{}) for a in range(45)];Araw=[s.SparseMatrix(45,45,{}) for a in range(45)];rawrows=0
for name,rows in d['source_Qx'].items():
 for row in rows:
  ww=row['word'];assert len(ww)==2 and all('__' not in z for z in ww);a=next(z for z in ww if z.startswith('C'));x=next(z for z in ww if z.startswith('x_'));assert set(ww)=={a,x};Rraw[int(a[1:])][xid[name],xid[x]]+=s.sympify(row['coefficient'],locals=loc);rawrows+=1
assert rawrows==29754
for name,rows in d['source_QC'].items():
 for row in rows:
  a,b=[int(z[1:]) for z in row['word']];v=s.sympify(row['coefficient'],locals=loc);Araw[a][int(name[1:]),b]+=v;Araw[b][int(name[1:]),a]-=v
R=[cl(Fx*sum((Tc[b,a]*Rraw[b] for b in range(45) if Tc[b,a]),s.zeros(328))*Tx) for a in range(45)]
A=[cl(Fc*sum((Tc[b,a]*Araw[b] for b in range(45) if Tc[b,a]),s.zeros(45))*Tc) for a in range(45)]
assert [enc(M) for M in R]==d['scalar_representation']
qC=defaultdict(list)
for a in range(45):
 for (out,b),v in A[a].todok().items():
  if a<b:qC[out].append(((a,b),v))
repcols=defaultdict(list)
for a,rr in enumerate(R):
 for (i,j),v in rr.todok().items():repcols[j].append((i,a,v))
def clean(z):return{k:s.expand(v) for k,v in z.items() if s.expand(v)!=0}
def canon(ww):
 if len(set(ww))!=len(ww):return None,0
 return tuple(sorted(ww)),(-1)**sum(a>b for j,a in enumerate(ww) for b in ww[j+1:])
def ce(z):
 # Component cochain action and antisymmetric bracket contraction.
 out=defaultdict(lambda:0)
 for (i,ww),v in z.items():
  for j,a,r in repcols[i]:
   qq,sg=canon((a,)+ww)
   if sg:out[j,qq]+=sg*r*v
  for k,c in enumerate(ww):
   rest=ww[:k]+ww[k+1:]
   for (a,b),r in qC[c]:
    qq,sg=canon((a,b)+rest)
    if sg:out[i,qq]-=(-1)**k*sg*r*v
 return clean(out)
def mulmask(left,right):
 if left&right:return 0,0
 return left|right,(-1)**sum((right&((1<<i)-1)).bit_count() for i in range(45) if left&(1<<i))
def leibniz(z):
 # Literal source-first odd polynomial. q(J_i) has J_j C_a; q on ghost
 # factors has minus from the leading odd J and the intervening C factors.
 out=defaultdict(lambda:0)
 for (i,ww),v in z.items():
  mask=sum(1<<a for a in ww)
  for j,a,r in repcols[i]:
   mm,sg=mulmask(1<<a,mask)
   if sg:out[j,tuple(a for a in range(45) if mm&(1<<a))]+=sg*r*v
  for k,c in enumerate(ww):
   before=sum(1<<a for a in ww[:k]);after=sum(1<<a for a in ww[k+1:])
   for pair,r in qC[c]:
    mm,sg=mulmask(before,sum(1<<a for a in pair))
    if not sg:continue
    nn,tt=mulmask(mm,after)
    if tt:out[i,tuple(a for a in range(45) if nn&(1<<a))]-=(-1)**k*sg*tt*r*v
 return clean(out)
diff=ce if role=='primary' else leibniz
def from_matrix(M):return{(i,(a,)):v for(i,a),v in M.todok().items()}
def from_vector(V):return{(i,()):v for(i,j),v in V.todok().items()}
def encode(z,degree):return{'shape':[328,math.comb(45,degree)],'ghost_degree':degree,'entries':[[i,list(ww),str(v)] for(i,ww),v in sorted(z.items())]}
def combine(a,b,factor=1):
 out=dict(a)
 for k,v in b.items():out[k]=out.get(k,0)+factor*v
 return clean(out)
outputs=[]
for probe,z in enumerate(d['outputs']):
 T=dec(d['source_vectors'][probe]);W0=dec(z['W0']);W2=dec(z['W2']);V={2:T,3:-T};U={2:cl(-W0-2*W2),3:cl(W0+W2)};rows={}
 for prime in [2,3]:
  v=from_vector(V[prime]);w=from_matrix(U[prime]);dv=diff(v);ddv=diff(dv);assert not ddv;h=combine(w,dv,-1);f=diff(w);dh=diff(h);assert dh==f;df=diff(f);assert not df
  wrong=combine(w,dv);omitU={k:-vv for k,vv in dv.items()};rows[str(prime)]={'V':enc(V[prime]),'U':enc(U[prime]),'dV':encode(dv,1),'H':encode(h,1),'F':encode(f,2),'dH':encode(dh,2),'dF':encode(df,3),'second_variation_residual':encode(combine(dh,f,-1),2),'wrong_source_orientation_changed_positions':len(combine(h,wrong,-1)),'omit_U_H_changed_positions':len(combine(h,omitU,-1)),'omit_U_F_changed_positions':len(f)}
 outputs.append({'probe':probe,'prime_logs':rows});print('STAGE IFC1 '+role+' complete source descent probe '+str(probe),flush=True)
out={'schema':'IFC1_MEASURED_LOCAL_CONVERSION_SOURCE_DESCENT','role':role,'source_Qx_rows':rawrows,'actual_Qx_only_x_C_source_projection_closed':True,'type_envelope':envelope,'Lorentz_scalar_source_types':allowed,'outputs':outputs,'source_Euler_sign':'POSITIVE_CSW','full_chiral_nilpotence_or_quantum_source_roots_measured':False};raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with(O/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'elapsed_after_imports':time.perf_counter()-tick,'packed_sha256':sha256(blob).hexdigest(),'raw_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True);timer.cancel()
