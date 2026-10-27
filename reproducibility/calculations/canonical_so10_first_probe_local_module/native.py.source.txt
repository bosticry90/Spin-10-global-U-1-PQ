from pathlib import Path
from hashlib import sha256
from collections import Counter,defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement
import gzip,json,sys,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];assert role in ['primary','replay']
for p,h in read(O/'preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==O and p.name.startswith('replay' if role=='primary' else'primary'):raise PermissionError('LFM1_PEER_DENIED')
sys.addaudithook(guard)
d=json.loads(gzip.decompress((O/(role+'_inputs.json.gz')).read_bytes()));g,xi,eta=s.symbols('g10 xi eta_H',real=True);loc={'g10':g,'xi':xi,'eta_H':eta}
spec={'P':(3,0,1),'KP':(3,-1,0),'B':(2,0,0),'x':(2,0,0),'C':(2,1,1),'a':(2,-1,1),'L':(4,0,0),'JB':(4,-1,1),'Jx':(4,-1,1),'JC':(4,-2,0),'Ja':(4,0,0),'JL':(2,-1,1),'u':(0,0,0),'rho':(2,1,1)}
other=sorted(set(spec)-{'P','KP','u','rho'})
def envelope(density_dim,ghost,parity):
 rows=set()
 for probe in ['u','rho']:
  remaining=2*density_dim-6-spec[probe][0]
  if role=='primary':
   multisets=[vv for n in range(remaining//2+1) for vv in combinations_with_replacement(other,n) if sum(spec[v][0] for v in vv)<=remaining]
  else:
   # Product of finite multivariate generating series, truncated by dimension.
   polynomial={(0,()):1}
   for v in other:
    new={}
    for (dd,word),co in polynomial.items():
     for n in range((remaining-dd)//spec[v][0]+1):new[dd+n*spec[v][0],word+(v,)*n]=co
    polynomial=new
   multisets=[word for dd,word in polynomial]
  for np in range(3):
   spin=['P']*np+['KP']*(2-np)
   for vv in multisets:
    fields=tuple(sorted([probe,*spin,*vv]));gh=sum(spec[v][1] for v in fields);pa=sum(spec[v][2] for v in fields)%2
    if gh!=ghost or pa!=parity:continue
    left=2*density_dim-sum(spec[v][0] for v in fields)
    if left<0 or left%2:continue
    for mass in range(left//2+1):rows.add((fields,mass,left//2-mass))
 return [{'fields':list(ww),'mass_degree':md,'ordinary_jet_degree':j} for ww,md,j in sorted(rows)]
breaking=envelope(5,1,1);counterterms=envelope(4,0,0)
@lru_cache(None)
def parse(z):return s.sympify(z,locals=loc)
dec=lambda z:s.SparseMatrix(*z['shape'],{(i,j):parse(c) for i,j,c in z['entries']});tidy=lambda M:s.SparseMatrix(M).applyfunc(s.expand)
def zero(M):assert not tidy(M).todok()
F=list(map(dec,d['F']));XS=[[dec(x) for x in row] for row in d['x_source']];Kvec=[{ch:list(map(dec,row[ch])) for ch in ['left','right']} for row in d['K_vector']];KM=list(map(dec,d['K_mass']));Swap=s.SparseMatrix(256,256,{(16*j+i,16*i+j):1 for i in range(16) for j in range(16)})
coefficient_counts={};all_degrees={}
for key,matrices,expectedg in [('F',F,0),('source_x',[x for row in XS for x in row],0),('vector_K',[x for row in Kvec for ch in ['left','right'] for x in row[ch]],3),('mass_K',KM,0)]:
 count=0;degrees=set()
 for M in matrices:
  for z in M.todok().values():
   assert z.free_symbols<={g,xi,eta};terms=s.Poly(z,g,xi,eta).terms();assert all(p[0]==expectedg and min(p)>=0 for p,c in terms);degrees.update(p for p,c in terms);count+=1
 coefficient_counts[key]=count;all_degrees[key]=[list(v) for v in sorted(degrees)]
for r in range(2):
 zero(F[r]-F[r].H);zero(Swap*KM[r]-KM[r]*Swap)
 for a in range(45):zero(XS[r][a]-XS[r][a].H);zero(Kvec[r]['left'][a]-Kvec[r]['left'][a].H);zero(Kvec[r]['right'][a]+Kvec[r]['left'][a].T)
src=d['source_primitive'];XX=[[s.zeros(16) for a in range(45)] for r in range(2)];source_pattern=Counter()
def co(cells):
 z=0
 for xp,ep,mask,n,den in cells:
  v=s.Rational(n,den)*xi**xp*eta**ep
  for k,p in enumerate([2,3,5,7]):
   if mask&(1<<k):v*=s.sqrt(p)
  if mask&16:v*=s.I
  z+=v
 return s.expand(z)
for i,j,p in src['X_plane_matrix']:
 for gp,w,ci in p['monomials']:
  assert gp==3 and len(w)==2 and all(not jet for n,jet in w);words=[src['names'][n] for n,jet in w];u=next(n for n in words if n.startswith('mw_u'));c=next(n for n in words if n.startswith('C'));XX[int(u[-1])][int(c[1:])][i,j]+=-s.I*co(p['coefficients'][ci])
for r in range(2):
 for a in range(45):zero(XX[r][a]-XS[r][a])
for lie,p in src['D_X']:
 for gp,w,ci in p['monomials']:
  words=[src['names'][n] for n,j in w];assert all(not j for n,j in w);u=sum(n.startswith('mw_u') for n in words);rho=sum(n.startswith('mw_rho') for n in words);cc=sum(n.startswith('C') for n in words);assert(u,rho,cc) in [(1,0,2),(0,1,1)];source_pattern['uCC_KPP' if u else'rhoC_KPP']+=1
# The concrete operator recipes fix dependency, type, normalization and order.
# Coefficients above are literal authenticated existing matrices, not new fits.
program=[{'term':'symmetric_kinetic','fields':['u','P','P'],'jet_degree':1,'mass_degree':0,'outer_g10_power':2,'normalization':'L_sym(F), derivative on both P legs with +/-1/2','coefficient':'F'}, {'term':'source_flow','fields':['u','C','KP','P'],'jet_degree':0,'mass_degree':0,'outer_g10_power':3,'normalization':'-i*KP*u*C*x_source*P; once','coefficient':'source_x'}, {'term':'vector','fields':['u','B','P','P'],'jet_degree':0,'mass_degree':0,'outer_g10_power':0,'normalization':'-i*u*B*barP*gamma*K_vector*P; K already g10^3','coefficient':'vector_K'}, {'term':'scalar','fields':['u','x','P','P'],'jet_degree':0,'mass_degree':0,'outer_g10_power':2,'normalization':'SMA alternating half once, K_mass(M(x)) and conjugate','coefficient':'mass_K'}]
allowedct={(tuple(x['fields']),x['mass_degree'],x['ordinary_jet_degree']) for x in counterterms}
for term in program:assert(tuple(sorted(term['fields'])),term['mass_degree'],term['jet_degree']) in allowedct
names=d['names'];pairs=d['geometry']['field_source_h_k'];sourcefield={J:i for i,J,h,k in pairs};fieldsource={i:J for i,J,h,k in pairs};physical={i for i,J,h,k in pairs};candidate_fields={i for i in physical if names[i].startswith(('B','x_','C'))};candidate_sources=set();ports=[]
for family in ['physical_G','physical_QG']:
 for r,p in enumerate(d[family]):
  deps={n for gp,w,ci in p['monomials'] for n,j in w};ss=set(deps)&set(sourcefield);conj={sourcefield[J] for J in ss};assert all(names[i].startswith(('bar','ub','b','L')) for i in conj)
  direct={(i,J) for i,J in fieldsource.items() if(i in candidate_fields and J in deps)or(J in candidate_sources and i in deps)}
  if role=='replay':
   via_sources={(sourcefield[J],J) for J in ss if sourcefield[J] in candidate_fields};assert direct==via_sources
  assert not direct
  add_a={i for i in physical if names[i].startswith(('bar','ub'))};bad_a={(i,fieldsource[i]) for i in add_a if fieldsource[i] in deps};add_JB={fieldsource[i] for i in physical if names[i].startswith('B')};bad_JB={(i,J) for i,J in fieldsource.items() if J in add_JB and i in deps}
  ports.append({'family':family,'r':r,'density_positions':len(p['monomials']),'source_coordinates':len(ss),'source_conjugate_fields':sorted(names[i] for i in conj),'candidate_BV_overlap_pairs':0,'add_antighost_control_pairs':len(bad_a),'add_vector_source_control_pairs':len(bad_JB)})
assert all(x['add_antighost_control_pairs'] and x['add_vector_source_control_pairs'] for x in ports)
out={'schema':'FIRST_PROBE_LOCAL_MODULE_INTEGRATION_V1','role':role,'breaking_type_envelope':breaking,'counterterm_type_envelope':counterterms,'concrete_functional_program':program,'coefficient_nonzero_positions':coefficient_counts,'coefficient_polynomial_degrees':all_degrees,'source_X_matches_actual_PMC_primitive':True,'measured_source_projection_patterns':dict(source_pattern),'all_coefficient_reality_and_mass_symmetry_pass':True,'actual_G_QG_vs_candidate_BV_ports':ports,'full_Q_assumed_nilpotent':False,'intrinsic_positive_coefficient_image_zero_by_unshifted_SMA_type_and_source_support':True,'ordinary_boundary_currents_reused':['PFJ symmetric kinetic IBP current','PFJ source Euler current','SMA alternating/hatted boundary; not deleted internally'],'new_quantum_coefficients_measured':False,'physical_or_authority_changed':False}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with(O/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'elapsed_after_imports':time.perf_counter()-tick,'packed_sha256':sha256(blob).hexdigest(),'raw_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
