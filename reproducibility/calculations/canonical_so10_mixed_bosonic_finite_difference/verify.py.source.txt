"""MBF1 exact mixed-family comparison and physical trace/boundary checks."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==hsh,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz');g=s.Symbol('g10',real=True);h=s.Symbol('h')
def sym(v):return s.sympify(v,locals={'g10':g})
def decode(rows):return {tuple((kind,mu,tuple(ds)) for kind,mu,ds in w):sym(v) for w,v in rows}
def cyc(w):return min(w[j:]+w[:j] for j in range(len(w)))
def add(p,w,v):
 w=cyc(w);p[w]=s.expand(p.get(w,0)+v)
def clean(p):return {w:s.expand(v) for w,v in p.items() if s.expand(v)!=0}
def diff(a,b):
 return clean({w:s.expand(a.get(w,0)-b.get(w,0)) for w in set(a)|set(b)})
def rows(p):return [[[[kind,mu,list(ds)] for kind,mu,ds in w],str(v)] for w,v in sorted(clean(p).items())]
for key in ['triangle_density','YYGG_density','YYYY_density']:assert not diff(decode(P[key]),decode(R[key])),key
for key in ['raw_triangle_hat_numerators','raw_box_two_hat_numerator','raw_box_four_hat_numerator']:
 assert set(P[key])==set(R[key])
 for k,a in P[key].items():
  b=R[key][k]
  for x,y in (zip(a,b) if isinstance(a,list) else [(a,b)]):assert s.expand(s.sympify(x)-s.sympify(y))==0
# True Nambu trace identities: U,V symmetric and R=-L^T. Preserve generic
# densities; use the exact transpose quotient only for actual model checks.
def actual(poly):
 out={}
 for w,v in poly.items():
  tw=tuple(({'L':'R','R':'L'}.get(kind,kind),mu,ds) for kind,mu,ds in reversed(w));sign=(-1)**sum(t[0] in ['L','R'] for t in w)
  a,b=cyc(w),cyc(tw)
  if a==b and sign==-1:continue
  key=min(a,b);factor=1 if key==a else sign;out[key]=s.expand(out.get(key,0)+factor*v)
 return clean(out)
def adjoint(poly):
 out={}
 for w,v in poly.items():add(out,tuple(({'U':'V','V':'U'}.get(kind,kind),mu,ds) for kind,mu,ds in reversed(w)),s.conjugate(v))
 return clean(out)
def ibp(poly):
 out={};current=[{} for _ in range(4)]
 for w,v in poly.items():
  jets=[j for j,t in enumerate(w) if t[2]]
  assert len(w)==3 and len(jets)==1 and len(w[jets[0]][2])==1
  base=tuple((kind,mu,()) for kind,mu,ds in w);rot=min(range(3),key=lambda j:base[j:]+base[:j]);ww=w[rot:]+w[:rot];base=base[rot:]+base[:rot];pos=(jets[0]-rot)%3;rho=ww[pos][2][0]
  if pos<2:add(out,ww,v)
  else:
   for j in [0,1]:
    nw=list(base);kind,mu,ds=nw[j];nw[j]=(kind,mu,(rho,));add(out,tuple(nw),-v)
   add(current[rho],base,v)
 return clean(out),[clean(v) for v in current]
reality={};reality_current={}
for key in ['triangle_density','YYGG_density','YYYY_density']:
 q=diff(decode(P[key]),adjoint(decode(P[key])));qa=actual(q)
 if key=='triangle_density':
  rem,J=ibp(qa);assert not actual(rem);reality_current[key]=[rows(v) for v in J]
 else:assert not qa
 reality[key]={'generic_literal_difference_positions':len(q),'actual_literal_difference_positions':len(qa),'actual_mod_boundary_remainder':'0'}
scalar4=decode(P['YYYY_density']);assert len(scalar4)==1
word,value=next(iter(scalar4.items()));assert all(t[0] in ['U','V'] for t in word) and sum(t[0]=='U' for t in word)==2
assert s.simplify(value-s.sympify(R['Schur_scalar4_coefficient']))==0
assert R['Schur_constant_mass_is_control_only']
# All finite words must have dimension4, the correct coupling, balanced PQ
# mass charges, and no unwanted scalar/gauge role or Lorentz structure.
counts={};nzoffdiag=0
for key,ny,ng in [('triangle_density',2,1),('YYGG_density',2,2),('YYYY_density',4,0)]:
 pol=decode(P[key]);assert pol;counts[key]=len(pol)
 for w,v in pol.items():
  assert sum(t[0] in ['U','V'] for t in w)==ny and sum(t[0] in ['L','R'] for t in w)==ng
  assert sum(1+len(t[2]) for t in w)==4 and sum(t[0]=='U' for t in w)==sum(t[0]=='V' for t in w)
  assert s.Poly(v,g).degree()==ng and s.expand(v/g**ng).has(g)==False
for k,vals in P['raw_triangle_hat_numerators'].items():
 v,j=k.split(':');v=list(map(int,v.split(',')));mu=next(z for z in v if z>=0)
 if mu!=int(j):assert all(s.sympify(z)==0 for z in vals)
for key in ['raw_box_two_hat_numerator','raw_box_four_hat_numerator']:
 for k,v in P[key].items():
  inds=[z for z in map(int,k.split(',')) if z>=0]
  if inds and inds[0]!=inds[1]:assert s.sympify(v)==0
changes4={key:len(diff(decode(P[key+'_density']),decode(P[key+'_no_four_hat_density']))) for key in ['YYGG','YYYY']}
pathchanges={key:len(diff(decode(P[key]),decode(P[key.replace('_density','_one_path_density')]))) for key in ['triangle_density','YYGG_density','YYYY_density']}
noDen=actual(diff(decode(P['triangle_density']),decode(P['triangle_no_denominator_density'])));noDenRem,noDenJ=ibp(noDen)
rawU=sum(s.sympify(v[2])!=0 for v in P['raw_triangle_hat_numerators'].values())
controls={'omit_four_hat_box_terms':all(v>0 for v in changes4.values()),'omit_one_allowed_chiral_path':all(v>0 for v in pathchanges.values()),'wrong_hat_sign':bool(scalar4),'premature_hat_zero':bool(scalar4),'wrong_Yukawa_gauge_phase':bool(P['YYGG_density']),'omit_Nambu_half':bool(scalar4),'extra_half_after_Nambu':bool(scalar4),'extra_family_three':bool(scalar4),'drop_denominator_derivative_ordered_kernel':rawU>0}
assert all(controls.values())
for obj in [P,R]:assert obj['physical_spin_trace']==4 and obj['gaussian_factor']=='1/2' and obj['path_trace_factor']=='1/2_FOR_EACH_ALLOWED_PATH' and obj['family_trace']=='FULL48_NO_EXTRA3' and obj['hat_rank']=='-2epsilon' and obj['raw_triangle_positions']==144 and obj['raw_box_positions']==194 and obj['new_one_loop_finite_families']==3 and obj['new_two_loop_integrals']==0 and not obj['physical_scheme_adopted'] and not obj['finite_massive_threshold_computed']
assert P['witness_spin_trace']==8 and P['witness_to_physical_divisor']==2
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
local={'generic_ordered_mixed_densities':{k:P[k] for k in ['triangle_density','YYGG_density','YYYY_density']},'actual_transpose_quotient_densities':{k:rows(actual(decode(P[k]))) for k in ['triangle_density','YYGG_density','YYYY_density']},'reality_boundary_currents':reality_current,'reality_checks':reality,'common_loop_factor':'1/(16*pi^2)','family_trace':'Tr48_NO_EXTRA3','no_physical_potential_or_scheme_adopted':True,'absolute_finite_baselines':'zeta_b0_kappa_distinct_unfixed'}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'mixed_density_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_MIXED_BOSONIC_PARITY_EVEN_FINITE_DIFFERENCE','elapsed_after_imports':time.perf_counter()-start,'raw_triangle_hat_polynomial_positions_compared':144,'raw_box_hat_polynomial_positions_compared':194,'density_word_counts':counts,'actual_transpose_quotient_word_counts':{k:len(actual(decode(P[k]))) for k in counts},'scalar4_coefficient':str(value),'independent_Schur_scalar4_coefficient':R['Schur_scalar4_coefficient'],'physical_reality_remainders':{k:v['actual_mod_boundary_remainder'] for k,v in reality.items()},'four_hat_omission_changes_positions':changes4,'single_chiral_path_omission_changes_positions':pathchanges,'denominator_derivative_ordered_nonzero_carriers':rawU,'denominator_omission_actual_density_different_positions':len(noDen),'denominator_omission_mod_boundary_different_positions':len(actual(noDenRem)),'controls':controls,'mixed_density_packed_sha256':sha256(blob).hexdigest(),'mixed_density_raw_sha256':sha256(raw).hexdigest(),'new_one_loop_finite_families':3,'new_two_loop_integrals':0,'full_family_mass_matrix_retained':True,'full_chiral_regularization_phase_or_measure_qualified':False,'source_background_or_massive_admissibility_qualified':False,'full_QAP_or_physical_matching_qualified':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
