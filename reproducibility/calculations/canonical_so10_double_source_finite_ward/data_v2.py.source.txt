from pathlib import Path
from hashlib import sha256
from collections import defaultdict,Counter
from functools import lru_cache
import json,gzip,os,sys,time,threading,itertools
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()));digest=lambda p:sha256(p.read_bytes()).hexdigest();g,xi,eta=s.symbols('g10 xi eta_H')
@lru_cache(maxsize=262144)
def co(z):return s.simplify(s.sympify(z))
def clean(p):return {w:co(z) for w,z in p.items() if co(z)}
def dec(m):return s.SparseMatrix(*m['shape'],{(i,j):co(z) for i,j,z in m['entries']})
def enc(m):return {'shape':list(m.shape),'entries':[[int(i),int(j),str(z)] for (i,j),z in sorted(m.todok().items())]}
def tidy(m):return s.SparseMatrix(m).applyfunc(co)
def zero(m):assert not tidy(m).todok()
def typ(n):
 for pre,k in [('JAp','Ja'),('JLp','JL'),('Bp','B'),('Lp','L'),('ap','a'),('Cp','C'),('Ap','A')]:
  if n.startswith(pre):return k
 if n.startswith('x_'):return 'X'
 raise AssertionError(('UNKNOWN_PHYSICAL_WORD',n))
def odd(n):return int(typ(n) in ['JL','a','C'])
def key(tok):
 n,jets=tok;k=typ(n);prefix={'Ja':0,'JL':1,'B':2,'L':3,'X':4,'a':5,'C':6,'A':7}[k]
 if k=='X':return (prefix,n,jets)
 digits=n[len({'Ja':'JAp','JL':'JLp','B':'Bp','L':'Lp','a':'ap','C':'Cp','A':'Ap'}[k]):];ids=tuple(map(int,digits.split('_')));return (prefix,ids,jets)
@lru_cache(maxsize=262144)
def canon(word):
 oslots=[t for t in word if odd(t[0])]
 if len(oslots)!=len(set(oslots)):return (),0
 phase=(-1)**sum(key(a)>key(b) for i,a in enumerate(oslots) for b in oslots[i+1:]);return tuple(sorted(word,key=key)),phase
def mulword(*words):return canon(tuple(t for w in words for t in w))
def addto(p,w,z):
 if z:p[w]=p.get(w,0)+z
def product(p,q):
 out={}
 for w,z in p.items():
  for v,y in q.items():
   word,ph=mulword(w,v)
   if ph:addto(out,word,ph*z*y)
 return clean(out)
def var(n,jets=()):return {((n,jets),):s.S.One}
def scale(p,z):return clean({w:v*z for w,v in p.items()})
def add(*ps):
 out={}
 for p in ps:
  for w,z in p.items():addto(out,w,z)
 return clean(out)
def serial(p):return [{'coefficient':str(z),'word':[n+('__'+'_'.join(map(str,j))) if j else n for n,j in w]} for w,z in sorted(clean(p).items(),key=lambda x:tuple(key(t) for t in x[0]))]
def token(n):
 z=n.split('__',1);return z[0],tuple(map(int,z[1].split('_'))) if len(z)==2 else ()
def fromrows(rows):
 out={}
 for row in rows:
  w,ph=canon(tuple(token(n) for n in row['word']))
  if ph:addto(out,w,ph*co(row['coefficient']))
 return clean(out)
def EL(p,n):
 out={}
 for w,z in p.items():
  prefix=0
  for k,(v,j) in enumerate(w):
   if v==n:
    assert not j
    ww,ph=canon(w[:k]+w[k+1:])
    if ph:addto(out,ww,z*ph*(-1)**(odd(n)*prefix))
   prefix+=odd(v)
 return clean(out)
def begin(role):
 t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation_v2.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def guard(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]));peer='replay' if role=='primary' else 'primary'
   if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('DSW1_PEER_DENIED')
 sys.addaudithook(guard);return t
def finish(role,d,t):
 d.update({'elapsed_after_imports':time.perf_counter()-t,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','absolute_Slavnov_QAP_E5A5_qualified':False})
 raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_v2_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'elapsed_after_imports':d['elapsed_after_imports'],'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
GROUPS=['GF_dB','GF_dA','GF_AB','GF_BB','GF_AA','GF_XX','GF_L','GF_aC','GF_Xv','source_Ja','source_JL']
def classify(w):
 kinds=sorted(typ(n) for n,j in w);nj=sum(len(j) for n,j in w)
 if kinds==['Ja'] and nj==0:return 'source_Ja'
 if kinds==['C','JL'] and nj==0:return 'source_JL'
 for ks,j,tag in [(['B'],1,'GF_dB'),(['A'],1,'GF_dA'),(['A','B'],0,'GF_AB'),(['B','B'],0,'GF_BB'),(['A','A'],0,'GF_AA'),(['X','X'],0,'GF_XX'),(['L'],0,'GF_L'),(['C','a'],0,'GF_aC'),(['X'],0,'GF_Xv')]:
  if kinds==ks and nj==j:return tag
 raise AssertionError(('UNCLASSIFIED_AUXILIARY_EULER',w,kinds,nj))
def charts(role):
 p=read(PK/f'frozen_a10_physical_reconciliation/full_{role}.json');Q=dec(p['C3_plane_to_parent']);old=read(PK/f'frozen_a10_e5_ghost_normalization/{role}.json')['ghost_metric'];EH,EM=dec(old['real_H_frame']),dec(old['real_heavy_frame']);E=EH.row_join(EM);e1=read(PK/f'frozen_a10_e1_fermion/{role}.json')['charts']['blocks'];QM=dec(e1['heavy_primal']['field_embedding'])
 if role=='primary':
  U=EM.T*QM;UH=EH.T*Q[:,:12];A=s.diag(UH.inv(),U.T);SP=A.inv().T;Ci=Q.inv()*E
 else:
  A=s.diag(dec(e1['light_primal']['left_section'])*EH,QM.T*EM);SP=s.diag(Q[:,:12].T*EH,dec(e1['heavy_dual']['field_embedding']).T*EM);Ci=dec(read(PK/f'frozen_a10_bv_master/{role}.json')['architecture']['plane_to_C3_field'])*E
 A,SP,Ci=map(tidy,[A,SP,Ci]);Cp=tidy(E.T*Q);zero(SP.T*A-s.eye(45));zero(Cp*Ci-s.eye(45));zero(Ci[:12,12:]);sub={}
 for i in range(45):
  ar=f'bar{i}' if i<12 else f'ub{i}';lr=f'b{i}' if i<12 else f'L{i}'
  for raw,pref,mat in [(ar,'ap',A),(lr,'Lp',A),('J'+ar,'JAp',SP),('J'+lr,'JLp',SP),(f'C{i}','Cp',Ci)]:sub[raw]={((pref+str(j),()),):z for (ii,j),z in mat.todok().items() if ii==i}
  for mu in range(4):sub[f'B{i}_{mu}']={((f'Bp{j}_{mu}',()),):z for (ii,j),z in Ci.todok().items() if ii==i}
 for i in range(12):
  for mu in range(4):sub[f'A{i}_{mu}']={((f'Ap{j}_{mu}',()),):z for (ii,j),z in Ci[:12,:12].todok().items() if ii==i}
 return A,SP,Ci,Cp,sub
def pull(rows,sub):
 out={}
 for row in rows:
  val={():co(row['coefficient'])}
  for raw in row['word']:
   n,j=token(raw)
   if n.startswith('x_'):term=var(n,j)
   else:
    assert n in sub,('UNMAPPED_RAW_FIELD',n)
    term={tuple((a,der+j) for a,der in w):z for w,z in sub[n].items()}
   val=product(val,term)
  for w,z in val.items():addto(out,w,z)
 return clean(out)
def combine(mat,ps):
 out=[{} for _ in range(mat.rows)]
 for (i,j),z in mat.todok().items():
  for w,v in ps[j].items():addto(out[i],w,z*v)
 return list(map(clean,out))
def columns(role):
 A,SP,Ci,Cp,sub=charts(role);raw=packed(CAL/f'canonical_so10_cutoff_source_ward_operator/{role}_inputs.json.gz');maps=raw['field_maps'];aux=[f'b{i}' if i<12 else f'L{i}' for i in range(45)];anti=[f'bar{i}' if i<12 else f'ub{i}' for i in range(45)]
 if role=='primary':
  eraw=[[] for _ in range(45)];found=Counter()
  for r,lam in enumerate(aux):
   for row in raw['GF']:
    for k,n in enumerate(row['word']):
     if token(n)[0]==lam:assert not token(n)[1];eraw[r].append({'coefficient':row['coefficient'],'word':row['word'][:k]+row['word'][k+1:]});found['GF']+=1
   for out,rs in maps.items():
    for row in rs:
     for k,n in enumerate(row['word']):
      if token(n)[0]==lam:
       assert not token(n)[1] and out in anti+aux
       eraw[r].append({'coefficient':row['coefficient'],'word':['J'+out]+row['word'][:k]+row['word'][k+1:]});found['source']+=1
 else:
  e2=read(PK/'frozen_a10_e2_transport/replay.json')['complete_columns'];eraw=[e2['J'+n]['source_polynomial'] for n in aux];assert all(e2['J'+n]['physical_program'] is None for n in aux);found={'full_E2_columns':45}
 E=combine(A.T,[pull(p,sub) for p in eraw]);QC=combine(Cp,[pull(maps[f'C{i}'] if role=='primary' else e2[f'C{i}']['source_polynomial'],sub) for i in range(45)]);groups={tag:[{} for _ in range(45)] for tag in GROUPS}
 for i,p in enumerate(E):
  for w,z in p.items():groups[classify(w)][i][w]=z
 for i in range(45):assert groups['source_Ja'][i]==scale(var(f'JAp{i}'),-1)
 return groups,QC,{'A':enc(A),'source_dual':enc(SP),'Cinv':enc(Ci),'Cphys':enc(Cp),'raw_derivative_audit':dict(found)}
def get_parent():
 table=packed(CAL/'canonical_so10_double_source_finite_contact/selected_double_source_finite_contact.json.gz')['relative_contact_without_g4_log2_16pi2'];p={}
 for i,j,k,l,z in table:p[((f'JLp{i}',()),(f'JLp{j}',()),(f'Cp{k}',()),(f'Cp{l}',()))]=co(z)
 return p
def summary(p):
 table=serial(p);return {'terms':len(table),'sha256':sha256((json.dumps(table,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()}
