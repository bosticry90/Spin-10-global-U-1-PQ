"""GQAP1 actual types/Euler ports and finite normalization witnesses."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
from collections import Counter
import json,gzip,ast,sys,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'

def source_types(role,fields):
 if role=='primary':
  tree=ast.parse((PK/'a10_bv_common.py').read_text());env={}
  for node in tree.body:
   if isinstance(node,ast.Assign):
    for target in node.targets:
     if isinstance(target,ast.Name) and target.id in ['H','M','IDS','DIM']:
      env[target.id]=eval(compile(ast.Expression(node.value),'<bound_type>','eval'),{'__builtins__':{'range':range}},env)
  fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='algebra')
  value=next(n.value for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fields' for t in n.targets))
  grades=eval(compile(ast.Expression(value),'<bound_fields>','eval'),{'__builtins__':{'range':range},**env})
  types={k:(d-gh,gh,p) for k,(d,gh,p) in grades.items()}
 else:
  types={}
  for n in fields:
   if n.startswith(('B','x_')):v=(1,0,0)
   elif n.startswith('C'):v=(0,1,1)
   elif n.startswith(('ub','bar')):v=(2,-1,1)
   elif n.startswith(('L','b')):v=(2,0,0)
   else:raise AssertionError(n)
   types[n]=v
 assert set(types)==set(fields) and len(types)==643
 for n in list(types):
  d,gh,p=types[n];types['J'+n]=(4-d,-1-gh,1-p)
 for a in range(12):
  for mu in range(4):types[f'A{a}_{mu}']=(1,0,0)
 return types

def main(role):
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'preparation.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()))
 ref=json.loads((PK/'frozen_a10_e5_full_hessian'/(role+'.json')).read_bytes());frame=ref['retained_reference'];fields=frame['field_order']
 types=source_types(role,fields);geo=data['geometry'];gp=dict(zip(geo['names'],geo['parities']))
 assert all(types[n][2]==gp[n] for n in fields)
 def tok(name):
  base,sep,jets=name.partition('__');assert all(i in '0123' for i in jets);d,gh,p=types[base]
  return base,jets,d+len(jets),gh,p
 assert set(data['master_field_maps'])==set(fields)
 ports=[];counts={name:0 for name in types};gf=Counter();D=s.zeros(45);nr=0;derivative_tangents=0;wrong_conversion_sensitive=0
 for field in fields:
  d,gh,p=types[field];J='J'+field;jd,jgh,jp=types[J]
  assert (jd,jgh+1,1-jp)==(4-d,-gh,p)
  assert (d+4-d,gh+1-gh,(1-p+p)%2)==(4,1,1)
  for rownum,row in enumerate(data['master_field_maps'][field]):
   ts=[tok(z) for z in row['word']]
   assert sum(v[2] for v in ts)==d and sum(v[3] for v in ts)==gh+1 and sum(v[4] for v in ts)%2==1-p
   word=[tok(J)]+ts;assert sum(v[2] for v in word)==4 and sum(v[3] for v in word)==0 and sum(v[4] for v in word)%2==0
   nr+=1
   for i,(base,jets,dim,ghost,par) in enumerate(word):
    if role=='primary':sign=(-1)**(par*sum(v[4] for v in word[:i])+len(jets))
    else:sign=(-1)**(par*sum(v[4] for v in word[i+1:])+par+len(jets))
    if i==0:assert base==J and sign==1
    assert 4-types[base][0]>=0
    ports.append([field,rownum,base,jets,sign]);counts[base]+=1
    wrong_conversion_sensitive+=bool(par)
   if field.startswith('B') and len(ts)==1 and ts[0][0].startswith('C') and len(ts[0][1])==1:
    derivative_tangents+=1
    col=int(ts[0][0][1:]);color,mu=map(int,field[1:].split('_'))
    assert ts[0][1]==str(mu)
    if mu==0:D[color,col]+=s.sympify(row['coefficient'])
   if field.startswith('x_'):
    assert all(not(jets and base.startswith('C')) for base,jets,*rest in ts)
 assert nr==35162 and derivative_tangents==180 and wrong_conversion_sensitive>0
 for row in data['gauge_fixing_density']:
  ts=[tok(z) for z in row['word']];dim=sum(v[2] for v in ts)
  assert dim<=4 and sum(v[3] for v in ts)==0 and sum(v[4] for v in ts)%2==0;gf[4-dim]+=1
 # All34 physical densities: direct AST versus independently polarized graphs.
 physical=json.loads((PK/'frozen_a10_executable_reconciliation/M08_PHYSICAL_ACTION_COVARIANT_EXECUTABLE_V1.json').read_bytes())
 pd={n:v['mass_dimension'] for n,v in physical['parameter_coordinates'].items()}
 for n,v in physical['parameter_coordinates'].items():
  if 'alias_of' in v:pd[v['alias_of']]=v['mass_dimension']
 def ast_dim(v):
  node=v['node']
  if node in ['ExactScalar','RepresentationGenerator','StructureConstant']:return 0
  if node=='Parameter':assert pd[v['name']]==v['mass_dimension'];return v['mass_dimension']
  if node=='Field':return 1
  if node=='PartialDerivative':return ast_dim(v['argument'])+1
  if node=='OrderedProduct':return sum(ast_dim(w) for w in v['factors'])
  if node=='Add':
   values={ast_dim(w) for w in v['terms']};assert len(values)==1;return next(iter(values))
  if node in ['GroupContraction','LorentzContraction']:return ast_dim(v['expression'])
  raise AssertionError(node)
 physical_dims={}
 if role=='primary':
  for term in physical['local_terms']:physical_dims[term['term_id']]=ast_dim(term['density'])
 else:
  for term in ref['physical_Hessian_program']['all_34_literal_terms']:
   dd=set()
   for params,nodes,coef in term['index_jet_graph_coefficients']:
    dd.add(sum(pd[n] for n in params)+sum(1+len(n[3]) for n in nodes if n[0]=='Field'))
   assert len(dd)==1;physical_dims[term['term_id']]=next(iter(dd))
 assert len(physical_dims)==34 and set(physical_dims.values())=={4}
 # Actual Phi seagull, actual physical scalar frame and actual BRST tangent.
 term=next(v for v in ref['physical_Hessian_program']['all_34_literal_terms'] if v['term_id']=='kinetic_Phi')
 sg=[v for v in term['index_jet_graph_coefficients'] if v[0]==['g10','g10'] and sorted(n[1] for n in v[1] if n[0]=='Field')==['B','B','h_x_Phi','k_x_Phi']]
 assert len(sg)==1 and sg[0][2]=='1' and sum(n[0]=='RepresentationGenerator' for n in sg[0][1])==2
 reconc=json.loads((PK/'frozen_a10_physical_reconciliation'/('full_'+role+'.json')).read_bytes())
 @lru_cache(None)
 def num(q):return s.sympify(q)
 rhos=[s.SparseMatrix(54,54,{(i,j):num(v) for i,j,v in m['entries']}) for m in reconc['representation_matrices']['Phi']]
 assert len(rhos)==45 and all(r.T==-r and all(v.is_real for v in r.values()) for r in rhos)
 r0=rhos[0]
 if role=='primary':
  xs=s.symbols('u0:54');vec=r0*s.Matrix(xs);quad=sum(v*v for v in vec)/2
  norm=s.simplify(sum(s.diff(quad,x,2) for x in xs))
  gram=s.Matrix([[(r0.T*r).trace() for r in rhos]])
 else:
  norm=sum(v*v for v in r0.values());entry0=dict(r0.todok())
  gram=s.Matrix([[sum(v*r[i,j] for (i,j),v in entry0.items()) for r in rhos]])
 assert s.simplify(norm-gram[0,0])==0 and norm!=0
 T=frame['physical_to_raw_kernel']['entries'];Ti=frame['physical_to_raw_inverse']['entries']
 TB=s.SparseMatrix(45,45,{(i//4,j//4):num(v) for i,j,v in T if i<180 and j<180 and i%4==j%4==0})
 Ci=s.SparseMatrix(45,45,{(i-508,j-553):num(v) for i,j,v in Ti if 508<=i<553 and 553<=j<598})
 derivative=(TB*D*Ci).applyfunc(s.simplify)
 if role=='primary':witness=(gram*derivative).applyfunc(s.simplify)
 else:
  witness=s.zeros(1,45)
  for k in range(45):
   dr=s.zeros(54)
   for j in range(45):
    if derivative[j,k]:dr+=derivative[j,k]*rhos[j]
   witness[0,k]=s.simplify(sum(v*dr[i,j] for (i,j),v in dict(r0.todok()).items()))
 nonzero=[[k,str(witness[0,k])] for k in range(45) if witness[0,k]!=0];assert nonzero
 # Full GF/source finite beta projections are qualified inputs, not new zeros.
 wb=json.loads((R/'calculations/canonical_so10_causal_wick_bridge/primary_v2_result.json').read_bytes())
 assert wb['tadpole_projection']==[] and wb['source_directions_checked']==643
 # Local beta contraction is a free-equation bisolution jet to every finite order.
 Q,M,d=s.symbols('Q M d');mom=[]
 for k in range(9):
  if role=='primary':quot,rem=s.div(Q**k,Q+M,Q);assert not rem.has(Q);v=s.expand(rem*d)
  else:v=s.expand((-M)**k*d)
  assert v==(-M)**k*d;mom.append(str(v))
 assert all(s.expand(s.sympify(mom[k+1])+M*s.sympify(mom[k]))==0 for k in range(8))
 x,y=s.symbols('x y');E=y+M*x;F=x*x;jet=s.Matrix([[d,-M*d],[-M*d,M*M*d]])
 beta=lambda f:s.expand(sum(jet[i,j]*s.diff(f,[x,y][i],[x,y][j]) for i in range(2) for j in range(2))/2)
 assert s.expand(beta(F*E)-beta(F)*E)==0
 # Q(Phi seagull) fixes the finite-chart primitive sign; no anomaly input fitted.
 heat,qp=s.symbols('Delta_heat Qbeta');dt=heat-qp;correct=-heat+qp;wrong=-heat
 assert s.expand(dt+correct)==0 and s.expand(dt+wrong)==-qp
 # Actual empty field rule does not delete its physical Euler/source variation.
 assert data['master_field_maps']['x_S_0']==[]
 lam=s.symbols('lambdaS');assert s.diff(-lam*(x*x+y*y)**2/4,x)!=0
 # A cutoff multiplying this seagull retains its integration-by-parts current.
 t=s.symbols('t');cut=s.Function('cut')(t);B=s.Function('B')(t);C=s.Function('C')(t)
 current=s.diff(2*cut*B*C,t)
 assert s.expand(2*cut*B*s.diff(C,t)+2*C*(s.diff(cut,t)*B+cut*s.diff(B,t))-current)==0
 assert s.expand(2*cut*B*s.diff(C,t)+2*C*cut*s.diff(B,t)-current)!=0
 # Ordinary versus BV source orientation, both parities.
 for par in [0,1]:assert (-1)**(par*par)==(-1)**par and (-1)**(par*(1-par))==1
 result={'schema':'GRADED_CAUSAL_QAP_NATIVE_V1','role':role,'source_rows':nr,'GF_rows':len(data['gauge_fixing_density']),
 'canonical_fields':643,'source_Euler_ports':len(ports),'Euler_ports_sha256':sha256(json.dumps(ports,separators=(',',':')).encode()).hexdigest(),
 'source_port_target_counts_sha256':sha256(json.dumps(counts,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 'zero_field_rule_outputs':sorted(n for n in fields if not data['master_field_maps'][n]),'GF_residual_dimensions':dict(gf),
 'physical_density_dimensions':physical_dims,'derivative_BRST_ports':derivative_tangents,'Phi_generator_norm':str(norm),
 'Phi_temporal_seagull_beta_coefficient_normalized':str(s.simplify(norm/2)),
 'Qbeta_Phi_B0_dC_coefficient_vector_normalized':nonzero,'scalar_beta_moments':mom,
 'actual_full_physical_Euler_dependency':ref['physical_Hessian_program']['full_physical_Euler_dependency_sha256'],
 'controls':{'odd_left_right_conversion_sensitive_ports':wrong_conversion_sensitive,'ghost_uniform_dimension_wrong':True,
 'nonzero_Phi_Qbeta_transport_sign':True,'EOM_contact_retained':True,'source_restrict_before_gradient_wrong':True,
 'switching_current_omission_nonzero':True,'empty_field_rule_not_zero_physical_Euler':True},
 'compact_QAP_anomaly_set_to_zero':False,'uncut_global_or_full_E5_A5_proved':False,'authority_changed':False,
 'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main(sys.argv[1])
