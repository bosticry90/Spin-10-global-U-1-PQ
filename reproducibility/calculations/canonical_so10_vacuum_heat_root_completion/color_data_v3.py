from data import *
from functools import lru_cache
CSW=CAL/'canonical_so10_cutoff_source_ward_operator';GTT=CAL/'canonical_so10_ghost_triangle_field_insertion'
@lru_cache(maxsize=131072)
def co(z):return s.simplify(s.sympify(z))
def dec(m):return s.SparseMatrix(*m['shape'],{(i,j):co(z) for i,j,z in m['entries']})
def clean(d):return {k:co(v) for k,v in d.items() if co(v)!=0}
def rows(d):return [[*k,str(v)] for k,v in sorted(clean(d).items())]
def begin3(role):
 t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation_v3.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def guard(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]));peer='color_replay_v3' if role=='primary' else 'color_primary_v3'
   if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('VHR1_COLOR_PEER_DENIED')
   if p.parent.name=='canonical_so10_ghost_vertex_order_reconciliation' and p.suffix=='.gz':raise PermissionError('VHR1_COLOR_TARGET_DENIED')
 sys.addaudithook(guard);return t
def finish3(role,out,t):
 out.update({'elapsed_after_imports':time.perf_counter()-t,'quantum_target_read':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'})
 raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/('color_'+role+'_v3_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'elapsed_after_imports':out['elapsed_after_imports'],'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
def raw_rules(maps):
 g=s.Symbol('g10');anti=[f'bar{a}' if a<12 else f'ub{a}' for a in range(45)];lam=[f'b{a}' if a<12 else f'L{a}' for a in range(45)];ai={n:i for i,n in enumerate(anti)};li={n:i for i,n in enumerate(lam)};B=[defaultdict(lambda:s.S.Zero) for mu in range(4)];L=defaultdict(lambda:s.S.Zero);N=defaultdict(lambda:s.S.Zero);cubic=0
 for r in range(45):
  for mu in range(4):
   for row in maps[f'B{r}_{mu}']:
    w=row['word']
    if len(w)!=2 or not any(n.startswith('B') for n in w):continue
    c=int(next(n for n in w if n.startswith('C'))[1:]);bn=next(n for n in w if n.startswith('B'));a,nu=map(int,bn[1:].split('_'));assert nu==mu;z=co(s.sympify(row['coefficient'])/g);assert not z.free_symbols;B[mu][r,a,c]+=z
  for row in maps[lam[r]]:
   w=row['word']
   if len(w)==3:cubic+=1;continue
   if len(w)!=2:continue
   cr=next(i for i,n in enumerate(w) if n.startswith('C'));ll=1-cr;c=int(w[cr][1:]);a=li[w[ll]];z=co(s.sympify(row['coefficient'])/g);assert not z.free_symbols;L[r,a,c]+=z
  for row in maps[anti[r]]:
   w=row['word']
   if len(w)!=2:continue
   cr=next(i for i,n in enumerate(w) if n.startswith('C'));ar=1-cr;c=int(w[cr][1:]);a=ai[w[ar]];z=co((-1 if cr>ar else 1)*s.sympify(row['coefficient'])/g);assert not z.free_symbols;N[r,a,c]+=z
 B=list(map(clean,B));assert all(x==B[0] for x in B);return B[0],clean(L),clean(N),cubic
def scalar_review(role,U):
 p=read(PK/'frozen_a10_physical_reconciliation'/('full_'+role+'.json'));v=dec(p['vacuum']['VEV']);Oraw=s.SparseMatrix(45,328,{});Oraw[12:,:]=dec(packed(CAL/'canonical_so10_vacuum_tangent_source_kernel'/(role+'_tables.json.gz'))['primitive_orbit_at_v']);O=U.T*Oraw;off=0;antisym_entries=0
 for sec,n in [('Phi',54),('Sigma',252),('phi',20),('S',2)]:
  for a,row in enumerate(p['representation_matrices'][sec]):
   m=dec(row);assert not (m+m.T).applyfunc(co).todok();delta=m*v[off:off+n,0]-O[a,off:off+n].T;assert not delta.applyfunc(co).todok();antisym_entries+=len(m.todok())
  off+=n
 H=dec(packed(CAL/'canonical_so10_yukawa_carrier_transport'/(role+'_tables.json.gz'))['H_new']);assert not (H.T*O).applyfunc(co).todok()
 return {'orbit_positions':45*328,'scalar_antisymmetry_full_positions':45*328**2,'scalar_sparse_entries':antisym_entries,'unbroken_projected_orbit_zero':True}
