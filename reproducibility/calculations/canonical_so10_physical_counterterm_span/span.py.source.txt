"""Actual parity-even physical/background counterterm span and parameter maps."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import gzip,json,sys,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
sys.path.insert(0,str(R/'tools/portable_dh_v1'))
from exact_algebra import Algebra,ONE,put,scale,scale_coefficient
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def plus(*pp):
 out={}
 for p in pp:
  for key,z in p.items():put(out,key,z)
 return out

def main():
 tick=time.perf_counter();watch=threading.Timer(120,lambda:os._exit(124));watch.daemon=True;watch.start();role=sys.argv[1];assert role in ['primary','replay'];prep=read(O/'preparation.json');assert digest(Path(__file__))==prep['source_sha256']
 for raw,h in prep['input_sha256'].items():assert digest(Path(raw))==h,raw
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  p=Path(os.fsdecode(args[0])).resolve()
  if len(args)>1 and isinstance(args[1],str) and any(c in args[1] for c in 'wax+'):raise PermissionError('PCS_NATIVE_WRITE')
  if p.suffix=='.json':assert str(p) in prep['read_json_by_role'][role],('PCS_UNDECLARED_JSON',str(p))
 sys.addaudithook(guard);get=lambda lab:read(Path(prep['artifacts'][role][lab]['path']))
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()));geo=data['geometry'];A=Algebra(geo['names'],geo['parities']);pairs=geo['field_source_h_k'];fields={i for i,J,h,k in pairs};sources={J for i,J,h,k in pairs};canonical=fields|sources;Jof={i:J for i,J,h,k in pairs};externalA={A.index[f'A{a}_{mu}'] for a in range(12) for mu in range(4)};omega={A.index[f'omega{a}'] for a in range(12)}
 def rows(rr):
  out={}
  for r in rr:
   for key,z in A.rows([r],explicit_g='g' in r).items():put(out,key,z)
  return out
 def elem(n,j=()):
  if isinstance(n,str):n=A.index[n]
  return {(0,((n,j),)):ONE}
 def pack(p):
  cc=[];ids={};rr=[]
  for(g,w),z in sorted(p.items()):
   if z not in ids:ids[z]=len(cc);cc.append([[*cell,v.numerator,v.denominator] for cell,v in z])
   rr.append([g,[[n,list(j)] for n,j in w],ids[z]])
  return {'coefficients':cc,'monomials':rr,'sha256_exact_cells':A.fingerprint(p)}
 def summary(p):return {'positions':len(p),'sha256_exact_cells':A.fingerprint(p)}
 def D(p,mu):
  out={}
  for(g,w),z in p.items():
   for at,(n,j) in enumerate(w):
    ww,sg=A.canonical(w[:at]+((n,tuple(sorted(j+(mu,)))),)+w[at+1:])
    if sg:put(out,(g,ww),scale_coefficient(z,sg))
  return out
 def DD(p,j):
  for mu in j:p=D(p,mu)
  return p
 def grad(p):
  out={}
  for(g,w),z in p.items():
   pref=0
   for at,(n,j) in enumerate(w):
    put(out.setdefault((n,j),{}),(g,w[:at]+w[at+1:]),scale_coefficient(z,(-1)**(A.parities[n]*pref)));pref+=A.parities[n]
  return {k:v for k,v in out.items() if v}
 def EL(p,domain):
  out={n:{} for n in domain}
  for(n,j),df in grad(p).items():
   if n in domain:
    for key,z in scale(DD(df,j),(-1)**len(j)).items():put(out[n],key,z)
  return out
 def vector(p):
  ef=EL(p,fields);ej=EL(p,sources);v={}
  for i in fields:v[i]=scale(ej[Jof[i]],-(-1)**A.parities[i]);v[Jof[i]]=scale(ef[i],(-1)**A.parities[i])
  return v
 def operation(images,odd=False):
  images={n:v for n,v in images.items() if v};cache={}
  def action(p):
   out={}
   if role=='replay':
    for(n,j),df in grad(p).items():
     if n in images:
      if(n,j) not in cache:cache[n,j]=DD(images[n],j)
      for key,z in A.product(cache[n,j],df).items():put(out,key,z)
    return out
   for(g,w),z in p.items():
    pref=0
    for at,(n,j) in enumerate(w):
     if n in images:
      if(n,j) not in cache:cache[n,j]=DD(images[n],j)
      pp=A.product(A.product({(g,w[:at]):scale_coefficient(z,(-1)**pref if odd else 1)},cache[n,j]),{(0,w[at+1:]):ONE})
      for key,c in pp.items():put(out,key,c)
     pref+=A.parities[n]
   return out
  return action
 from fractions import Fraction
 import itertools
 def scalar(co):
  out=0
  for(xi,eta,m),v in co:
   assert xi==eta==0
   out+=s.Rational(v.numerator,v.denominator)*s.prod(s.sqrt(p) if bit<4 else s.I for bit,p in enumerate([2,3,5,7,-1]) if m&(1<<bit))
  return s.expand(out)
 def mat(packet):
  m=s.zeros(*packet['shape'])
  for i,j,z in packet['entries']:m[i,j]=s.sympify(z)
  return m
 def mpack(m):return {'shape':list(m.shape),'entries':[[i,j,str(s.simplify(m[i,j]))] for i in range(m.rows) for j in range(m.cols) if m[i,j]!=0]}
 def GD(p):return {(g,w):scale_coefficient(co,g) for(g,w),co in p.items() if g}
 def DG(p):
  out={}
  for(g,w),co in p.items():
   if g:put(out,(g-1,w),scale_coefficient(co,g))
  return out
 def canon_source_image(v):return scale(plus(*(A.product(elem(Jof[i]),scale(pp,(-1)**A.parities[i])) for i,pp in v.items() if pp)),-1)
 print('STAGE '+role+' independent_background_field_Ward_and_complete_carriers',flush=True)
 e1=get('e1');e2=get('e2');e3=get('e3');action=get('action');rz={i:rows(data['master_field_maps'][A.names[i]]) for i in fields};q=operation(rz,True)
 tp={A.index[n]:rows(rr) for n,rr in e3['operators']['Tq_transported'].items()};tb={A.index[n]:rows(rr) for n,rr in e3['operators']['Tb_geometric_and_transported'].items()};db={n:plus(tb.get(n,{}),scale(tp.get(n,{}),-1)) for n in fields|externalA};DB=operation(db)
 physical={i for i in fields if A.names[i].startswith(('B','x_'))};assert len(physical)==508 and all(not db[i] for i in physical) and all(db[n]==tb[n] for n in externalA)
 coarse=set();placements=set()
 for count in range(5):
  for word in itertools.combinations_with_replacement(['A','B','x'],count):
   for orders in itertools.product(range(5-count),repeat=count):
    d=sum(orders);rank=sum(t!='x' for t in word)+d
    if count+d<=4 and rank%2==0:
     coarse.add((word.count('A'),word.count('B'),word.count('x'),d,4-count-d,rank));placements.add(tuple(sorted(zip(word,orders))))
 assert (0,0,2,2,0,2) in coarse and (0,2,0,2,0,4) in coarse and (1,0,2,1,0,2) in coarse
 # Metric-pairing tensors cannot produce epsilon0123: all three pairings
 # vanish on four distinct indices. Internal epsilon10 is a different tensor.
 assert all(all(i!=j for i,j in pairing) for pairing in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]])
 print('STAGE '+role+' actual_H_metric_linear_space_and_Casimir_ideals',flush=True)
 f={};hids={A.index[f'C{i}']:i for i in range(12)}
 for a in range(12):
  for(g,w),co in rz[A.index[f'C{a}']].items():
   if all(n in hids for n,j in w):
    assert g==1 and len(w)==2 and all(not j for n,j in w)
    b,c=[hids[n] for n,j in w];v=-scalar(co);f[a,b,c]=v;f[a,c,b]=-v
 ad=[s.Matrix(12,12,lambda i,j:f.get((i,a,j),0)) for a in range(12)];G=mat(e1['charts']['blocks']['light_primal']['invariant_bilinear']);tau=mat(e1['charts']['blocks']['light_primal']['conjugation']);assert G.det()!=0
 assert all(m.T*G+G*m==s.zeros(12) for m in ad)
 killing=s.Matrix(12,12,lambda i,j:-s.trace(ad[i]*ad[j]));cas=G.inv()*killing;eigs=cas.eigenvals();assert sorted(eigs.values())==[1,3,8] and len(eigs)==3
 metrics={};projectors={}
 for value,mult in eigs.items():
  pr=s.eye(12)
  for other in eigs:
   if value!=other:pr=pr*(cas-other*s.eye(12))/(value-other)
  pr=s.simplify(pr);gg=s.simplify(G*pr);assert pr*pr==pr and pr.rank()==mult and gg==gg.T and all(m.T*gg+gg*m==s.zeros(12) for m in ad)
  assert s.simplify(tau.T*s.conjugate(gg)*tau-gg)==s.zeros(12)
  metrics[mult]=gg;projectors[mult]=pr
 assert sum(projectors.values(),s.zeros(12))==s.eye(12) and killing.rank()==11
 keys=list(itertools.combinations_with_replacement(range(12),2));ix={key:i for i,key in enumerate(keys)};constraints=[]
 for m in ad:
  for i,j in keys:
   row=[0]*len(keys)
   for k in range(12):row[ix[tuple(sorted((k,j)))]]+=m[k,i];row[ix[tuple(sorted((i,k)))]]+=m[k,j]
   if any(row):constraints.append(row)
 if role=='primary':
  from sympy.polys.matrices import DomainMatrix
  null=DomainMatrix.from_Matrix(s.Matrix(constraints),extension=True).to_field().nullspace(divide_last=True).to_Matrix();assert null.rows==3
  basis=s.Matrix([[gg[i,j] for gg in metrics.values()] for i,j in keys]);assert basis.rank()==3 and basis.row_join(null.T).rank()==3
 else:
  # Independent upper bound uses the inherited actual H=su3+su2+u1 with
  # these verified Casimir ideals, rather than reading primary null vectors.
  assert [projectors[k].rank() for k in [1,3,8]]==[1,3,8] and all(pr*m==m*pr for pr in projectors.values() for m in ad)
  assert all(projectors[1]*m==s.zeros(12) for m in ad)
 print('STAGE '+role+' exact_scalar_and_vector_gauge_completion_controls',flush=True)
 xx,yy,dx,dy,bb,om,dom,ga,aa,cc=s.symbols('x y dx dy B omega domega g a b');j=s.Matrix([[0,-1],[1,0]]);xs=s.Matrix([xx,yy]);ds=s.Matrix([dx,dy]);delta_x=-ga*om*j*xs;delta_d=-ga*(dom*j*xs+om*j*ds);L=(ds.dot(ds))/2+aa*ga*bb*ds.dot(j*xs)+cc*ga**2*bb**2*xs.dot(xs)/2
 delta=s.expand(sum(s.diff(L,z)*v for z,v in zip([xx,yy,dx,dy,bb],[*delta_x,*delta_d,dom])));assert s.expand(delta-dom*(ga*(aa-1)*ds.dot(j*xs)+ga**2*(cc-aa)*bb*xs.dot(xs)))==0
 assert delta.subs({aa:1,cc:1})==0 and s.expand(delta.subs({aa:0,cc:1}))!=0 and s.expand(delta.subs({aa:1,cc:0}))!=0
 Z=s.Matrix(s.symbols('z0:3'));K=s.Matrix(s.symbols('k0:3'));T=s.Matrix(s.symbols('t0:3'));O=s.Matrix(s.symbols('o0:3'));dz=ga*Z.cross(O)-ga*T;dk=T+ga*K.cross(O)
 var=s.expand(Z.dot(dz)+aa*ga*(dz.dot(K)+Z.dot(dk))+cc*ga**2*K.dot(dk));expect=ga*(aa-1)*Z.dot(T)+ga**2*(cc-aa)*K.dot(T);assert s.expand(var-expect)==0 and s.expand(var.subs({aa:1,cc:1}))==0
 print('STAGE '+role+' actual_scalar_dilations_and_weighted_coupling_package',flush=True)
 Psi=plus(*(rows(rr) for rr in e1['polynomial_parts'].values()));gf=rows(data['gauge_fixing_density']);shifts={A.index[n]:rows(rr) for n,rr in e2['source_shifts'].items()};fullq={**rz,**{A.index[n]:rows(entry['source_polynomial']) for n,entry in e2['complete_columns'].items()}};Qpoly=operation(fullq,True)
 sourceS=plus(*(A.product(elem(Jof[i]),rz[i]) for i in fields));defs={};basis={};vfields={}
 for sec,size in [('Phi',54),('Sigma',252),('phi',20),('S',2)]:
  v={i:elem(i) for i in fields if A.names[i].startswith('x_'+sec+'_')};assert len(v)==size;K0=canon_source_image(v);V=operation(vector(K0));W=V(Psi);gen=plus(K0,W);vec=vector(gen)
  N=scale(plus(*(A.product(shifts[Jof[i]],pp) for i,pp in v.items())),-1);assert W==N
  for i in fields:assert not plus(q(vec[i]),scale(V(rz[i]),-1))
  assert not Qpoly(gen)
  trace=plus(*(grad(vec[i]).get((i,()),{}) for i in fields));assert trace=={(0,()):scale_coefficient(ONE,size)}
  basis[sec]=gen;vfields[sec]=vec;defs[sec]={'K0':pack(K0),'W':pack(W),'generator':pack(gen),'all1286_columns':{A.names[n]:pack(pp) for n,pp in vec.items() if pp},'field_trace':size,'source_and_gauge_fixing_Q_image_zero_without_physical_Euler_programs':True}
 vg={i:elem(i) for i in fields if A.names[i].startswith(('B','C'))};assert len(vg)==225;Kg0=canon_source_image(vg);V=operation(vector(Kg0));Wg=plus(V(Psi),scale(GD(Psi),-1));Kg=plus(Kg0,Wg);vKg=vector(Kg)
 for i in fields:assert not plus(q(vKg[i]),scale(V(rz[i]),-1),GD(rz[i])),('COUPLING_FIELD_RULE',A.names[i])
 trace=plus(*(grad(vKg[i]).get((i,()),{}) if not A.parities[i] else scale(grad(vKg[i]).get((i,()),{}),-1) for i in fields));assert trace=={(0,()):scale_coefficient(ONE,135)}
 qkg=Qpoly(Kg);qsrc={key:co for key,co in qkg.items() if any(n in sources for n,j in key[1])};qgf={key:co for key,co in qkg.items() if not any(n in sources for n,j in key[1])}
 thetaS=[]
 for mu in range(4):thetaS.append(plus(*(A.product(elem(Jof[A.index[f'B{a}_{mu}']]),elem(f'C{a}')) for a in range(45))))
 assert not plus(qsrc,GD(sourceS),scale(plus(*(D(p,mu) for mu,p in enumerate(thetaS))),-1))
 Lcur=[rows(rr) for rr in e2['action_density_boundary']];EGF=plus(GD(gf),scale(V(gf),-1));ELcur=[plus(GD(p),scale(V(p),-1)) for p in Lcur];assert not plus(EGF,q(Wg),scale(plus(*(D(p,mu) for mu,p in enumerate(ELcur))),-1))
 thetaGF=[{} for _ in range(4)]
 for(i,jets),df in grad(gf).items():
  assert len(jets)<=1
  if jets and i in fields and vKg[i]:thetaGF[jets[0]]=plus(thetaGF[jets[0]],A.product(vKg[i],df))
 completeGFcur=[plus(a,b) for a,b in zip(ELcur,thetaGF)];assert not plus(GD(gf),qgf,scale(plus(*(D(p,mu) for mu,p in enumerate(completeGFcur))),-1))
 wrong=scale(q(GD(Psi)),2);witness=next(({'field':A.names[n],'Euler':summary(pp)} for n,pp in EL(wrong,fields).items() if pp),None);assert witness
 wrongg=plus(GD(sourceS),scale(DG(sourceS),-1));assert wrongg
 print('STAGE '+role+' potential_companion_counts_and_mixed_background_falsifiers',flush=True)
 table=[]
 for term in action['local_terms']:
  if term['sector']!='PARENT_SCALAR_POTENTIAL':continue
  stack=[term['term']['density']];counts=Counter()
  while stack:
   node=stack.pop()
   if isinstance(node,list):stack.extend(node)
   elif isinstance(node,dict):
    if node.get('node')=='Field':counts[node['name'].removesuffix('Bar')]+=1
    else:stack.extend(node.values())
  label=term['coefficient_direction'];parts=['real','imag'] if term['term']['complex_monomial'] else ['real']
  for part in parts:table.append({'coupling':label,'component':part,'counts':{sec:counts[sec] for sec in ['Phi','Sigma','phi','S']},'field_degree':sum(counts.values())})
 assert len(table)==34
 pars=s.symbols('p0:34');t=s.symbols('t0:34');z=s.symbols('z0:4');fY=s.Symbol('fY');sectors=['Phi','Sigma','phi','S'];dpar=[-t[a]-pars[a]*sum(z[i]*table[a]['counts'][sec] for i,sec in enumerate(sectors))/2 for a in range(34)];dg=-ga*fY/2
 assert all(s.expand(dpar[a]+t[a]+pars[a]*sum(z[i]*table[a]['counts'][sec] for i,sec in enumerate(sectors))/2)==0 for a in range(34)) and s.expand(dg+ga*fY/2)==0
 ref=get('ref')['retained_reference'];raw=ref['field_order'];Tmap={}
 for a,jj,coef in ref['physical_to_raw_kernel']['entries']:Tmap.setdefault(a,[]).append((jj,rows([{'word':[],'coefficient':coef}])))
 px={a:plus(*(A.product(co,elem(raw[jj])) for jj,co in Tmap[a])) for a in range(180,508)};x=px[506];y=px[507]
 center=metrics[1];row=next(i for i in range(12) if any(center[i,j]!=0 for j in range(12)));ell=[s.simplify(center[row,j]) for j in range(12)];wcenter=plus(*(A.product(rows([{'word':[],'coefficient':str(co)}]),elem('omega'+str(j))) for j,co in enumerate(ell) if co));ac=[plus(*(A.product(rows([{'word':[],'coefficient':str(co)}]),elem(f'A{j}_{mu}')) for j,co in enumerate(ell) if co)) for mu in range(4)]
 assert all(DB(a)==D(wcenter,mu) for mu,a in enumerate(ac))
 currents=[scale(plus(A.product(y,D(x,mu)),scale(A.product(x,D(y,mu)),-1)),4) for mu in range(4)];mixed=plus(*(scale(A.product(ac[mu],currents[mu]),1 if mu==0 else -1) for mu in range(4)));mixedEL=EL(DB(mixed),omega);mixedWitness=next(({'omega':A.names[n],'Euler':summary(p)} for n,p in mixedEL.items() if p),None);assert mixedWitness
 rad=plus(A.product(x,x),A.product(y,y));amass=plus(*(scale(A.product(A.product(ac[mu],ac[mu]),rad),1 if mu==0 else -1) for mu in range(4)));massWitness=next(({'omega':A.names[n],'Euler':summary(p)} for n,p in EL(DB(amass),omega).items() if p),None);assert massWitness
 puremass=plus(*(scale(A.product(ac[mu],ac[mu]),1 if mu==0 else -1) for mu in range(4)));long=plus(*(scale(D(ac[mu],mu),1 if mu==0 else -1) for mu in range(4)));longsq=A.product(long,long);assert any(EL(DB(puremass),omega).values()) and any(EL(DB(longsq),omega).values())
 # Four quadratic PQ singlets supply four kinetic metrics after the complete
 # Noether census; a real symmetric2x2 copy metric must commute with qJ.
 u0,u1,u2=s.symbols('u0:3');mm=s.Matrix([[u0,u1],[u1,u2]]);assert s.solve(list(mm*j-j*mm),[u1,u2])=={u1:0,u2:u0}
 eps,traceTerm=s.symbols('epsilon traceTerm');X0,Y0,mu0,lam0=s.symbols('X Y m2 lambda');rs=X0**2+Y0**2;S0=mu0*rs/2+lam0*rs**2/4;HH=s.hessian(S0,[X0,Y0]);DD=HH.det();deform=s.hessian(-(X0*s.diff(S0,X0)+Y0*s.diff(S0,Y0)),[X0,Y0]);rawresponse=s.cancel(s.trace(HH.inv()*deform)/2);canonical=s.cancel(-(X0*s.diff(DD,X0)+Y0*s.diff(DD,Y0))/(2*DD));assert s.cancel(rawresponse-canonical)==-2
 point={X0:1,Y0:2,mu0:3,lam0:1};gaussian={'raw_descendant':str(rawresponse.subs(point)),'canonical':str(canonical.subs(point)),'necessary_measure_difference':'-2'};assert gaussian['raw_descendant']=='-83/24' and gaussian['canonical']=='-35/24'
 programs=[]
 for i in sorted(physical):
  pr=e2['complete_columns'][A.names[Jof[i]]]['physical_program'];assert pr;programs.append({'field':A.names[i],'physical_program_sha256':sha256(json.dumps(pr,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
 result={'schema':'PHYSICAL_COUNTERTERM_SPAN_V1','route':role,'scientific_disposition':'ACTUAL_FORMAL_PARITY_EVEN_ONE_LOOP_PHYSICAL_PARAMETER_SPAN_AND_FIRST_ORDER_NORMALIZATION_RECONSTRUCTION_WITH_SEPARATE_BACKGROUND_VACUUM_NORMALIZATIONS_NOT_FULL_E5',
 'physical508_background48_difference_Ward_checked':True,'raw_carrier_census':[list(p) for p in sorted(coarse)],'ordinary_jet_placement_count':len(placements),'actual_H_invariant_metric_real_dimension':3,'H_Killing_rank':11,'H_metric_ideal_dimensions':[1,3,8],'H_metric_projectors':{str(k):mpack(pr) for k,pr in projectors.items()},'H_metric_basis':{str(k):mpack(gg) for k,gg in metrics.items()},'H_Casimir_eigenvalues':sorted([[str(k),v] for k,v in eigs.items()]),'H_adjoint_matrices':[mpack(m) for m in ad],'scalar_completion_coefficients':[1,1],'vector_completion_coefficients':[1,1],'actual_metric_parity_cannot_generate_epsilon0123':True,'four_actual_scalar_dilations':defs,'coupling_generator':{'K0':pack(Kg0),'W':pack(Wg),'generator':pack(Kg),'all1286_columns':{A.names[n]:pack(pp) for n,pp in vKg.items() if pp},'all643_weighted_field_relations':True,'field_supertrace':135,'source_current':[pack(p) for p in thetaS],'complete_GF_current':[pack(p) for p in completeGFcur],'omitted_g_dPsi_nonboundary_control':witness,'missing_g_factor_source_control':summary(wrongg)},'real34_potential_companion_count_table':table,'parameter_shift_formula':'delta_g=-g*f/2;delta_lambda_a=-t_a-lambda_a*sum_s z_s*n_sa/2;Hnorm=-(f*Kgstar+sum_s z_s*Ks)/2;B_PQ=delta_p S+QHnorm+N[A]+c modulo currents','mixed_abelian_current_Ward_failure':mixedWitness,'mixed_A2_scalar_Ward_failure':massWitness,'vector_mass_and_longitudinal_controls_nonzero':True,'scalar_kinetic_metric_directions':4,'physical_YM_metric_directions':1,'physical_potential_real_directions':34,'pure_background_metric_directions':3,'field_independent_normalization_kept_separate':True,'gaussian_nonzero_trace_control':gaussian,'all508_physical_Euler_programs':programs,'unit_generators':'[Ks]=Ks+hbar*I_Ws;[Kgstar]=Kgstar+hbar*I_Wg;whole sourcefree W insertion retained in same T_kappa;nonzero raw field traces/reference/heat response retained','parameter_scope':'constant physical parameter derivative of complete same prescribed family;Gamma_ref,heat and finite conversion derivatives kept;NOT local g(x) QAP','actual_R_coefficients_beta_functions_or_finite_values_extracted':False,'full_E5_A5_universal_source_adequacy_all_order_or_physical_viability_proved':False,'authority_changed':False,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);watch.cancel()
if __name__=='__main__':main()
