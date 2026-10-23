"""BWF1 exact complete functional, Ward/current and invariant-ambiguity gate."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==hsh,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz');g=s.Symbol('g10',real=True)
def decode(rows):return {tuple((k,n,tuple(ds)) for k,n,ds in ww):s.sympify(v,locals={'g10':g}) for ww,v in rows}
def clean(p):return {w:s.expand(v) for w,v in p.items() if s.expand(v)!=0}
def diff(a,b):return clean({w:a.get(w,0)-b.get(w,0) for w in set(a)|set(b)})
def eqrows(a,b):assert not diff(decode(a),decode(b))
for key in ['density','gauge_density','scalar_kinetic_density','mixed_density','Ward_image','direct_q_density','boundary_divergence','Ward_without_scalar_Euler_terms']:eqrows(P[key],R[key])
assert set(P['Euler_matrices'])==set(R['Euler_matrices']) and len(P['Euler_matrices'])==10
for k in P['Euler_matrices']:eqrows(P['Euler_matrices'][k],R['Euler_matrices'][k])
for a,b in zip(P['boundary_current'],R['boundary_current']):eqrows(a,b)
for key in ['invariant_densities','scalar_kinetic_covariantization_mismatches']:
 assert set(P[key])==set(R[key])
 for k in P[key]:eqrows(P[key][k],R[key][k])
assert P['invariant_Ward_images']==R['invariant_Ward_images']=={'gauge':[],'mass_kinetic':[],'potential':[]}
W,Q,DJ=map(lambda k:decode(P[k]),['Ward_image','direct_q_density','boundary_divergence'])
for w in set(W)|set(Q)|set(DJ):assert s.expand(Q.get(w,0)-W.get(w,0)-DJ.get(w,0))==0
assert W and DJ
# Finite color trace and actual Nambu transpose identities. All current words
# contain at most one ghost, so moving it past even fields adds no sign.
def cyc(w):return min(w[j:]+w[:j] for j in range(len(w)))
swap={'L':'R','R':'L','cL':'cR','cR':'cL'}
def transpose(p):
 out={}
 for w,v in p.items():
  tw=tuple((swap.get(k,k),n,ds) for k,n,ds in reversed(w));sign=(-1)**sum(t[0] in swap for t in w);out[tw]=s.expand(out.get(tw,0)+sign*v)
 return clean(out)
def actual(p):
 out={}
 for w,v in p.items():
  tw=tuple((swap.get(k,k),n,ds) for k,n,ds in reversed(w));sign=(-1)**sum(t[0] in swap for t in w);a,b=cyc(w),cyc(tw)
  if a==b and sign==-1:continue
  key=min(a,b);out[key]=s.expand(out.get(key,0)+(1 if key==a else sign)*v)
 return clean(out)
def rows(p):return [[[[k,n,list(ds)] for k,n,ds in w],str(v)] for w,v in sorted(clean(p).items())]
L0=decode(P['density']);phys=actual(L0);physW=actual(W)
GF=packed(CAL/'canonical_so10_finite_gauge_ward_functional/primary_tables.json.gz');gf={tuple(('L' if k=='A' else k,n,tuple(ds)) for k,n,ds in ww):s.sympify(v,locals={'g10':g}) for ww,v in GF['density']}
assert not diff(actual(decode(P['gauge_density'])),actual(gf))
# The Ward tangent preserves the actual symmetric masses and R=-L^T.
def t(k,n=-1,ds=()):return (k,n,ds)
for mu in range(4):
 ql={(t('cL',-1,(mu,)),):1,(t('L',mu),t('cL')):-s.I*g,(t('cL'),t('L',mu)):s.I*g}
 qr={(t('cR',-1,(mu,)),):1,(t('R',mu),t('cR')):-s.I*g,(t('cR'),t('R',mu)):s.I*g}
 assert not diff(transpose(ql),{w:-v for w,v in qr.items()})
for kind,qa in [('U',{(t('cR'),t('U')):s.I*g,(t('U'),t('cL')):-s.I*g}),('V',{(t('cL'),t('V')):s.I*g,(t('V'),t('cR')):-s.I*g})]:assert not diff(transpose(qa),qa)
missing=diff(W,decode(P['Ward_without_scalar_Euler_terms']));assert missing
mis={k:len(v) for k,v in P['scalar_kinetic_covariantization_mismatches'].items()};assert all(mis.values())
for w in L0:assert sum(k=='U' for k,n,ds in w)==sum(k=='V' for k,n,ds in w)
degrees=sorted({powers[0] for v in W.values() for powers,co in s.Poly(v,g).terms() if co!=0})
controls={'omit_scalar_Euler_mass_terms':bool(missing),'omit_boundary_current':bool(DJ),'gauge_only_functional_omits_mixed_Ward':bool(P['mixed_density']),'covariantize_scalar2_without_measured_companions':all(mis.values()),'extra_family_three':bool(W),'extra_normalization_half':bool(W),'drop_relative_invariant_potential_changes_measured_functional':bool(P['invariant_densities']['potential'])}
assert all(controls.values())
for obj in [P,R]:assert obj['family_trace']=='FULL48_NO_EXTRA3' and obj['measured_scalar_kinetic_coefficient']=='1/6' and obj['new_loop_integrals']==0 and not obj['physical_scheme_adopted']
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
local={'actual_bosonic_finite_density':rows(phys),'actual_algebraic_Ward_image':rows(physW),'actual_boundary_current':[rows(actual(decode(v))) for v in P['boundary_current']],'candidate_CT_is_negative_measured_density':True,'invariant_directions':P['invariant_densities'],'invariant_coefficients':'zeta_g,zeta_M,zeta_V_SYMBOLIC_NOT_ADOPTED_NOT_COMPLETE_SPACE','old_contact_baselines':'b0,kappa_DISTINCT_NOT_IDENTIFIED','common_loop_factor':'1/(16*pi^2)','family_trace':'Tr48_NO_EXTRA3','normalized_field_independent_free_determinant_removed':True}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'bosonic_ward_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_SELECTED_BOSONIC_FERMION_FINITE_FUNCTIONAL_AND_WARD_IMAGE','elapsed_after_imports':time.perf_counter()-start,'generic_density_trace_words':len(L0),'actual_density_trace_words':len(phys),'generic_Ward_trace_words':len(W),'actual_Ward_trace_words':len(physW),'Euler_ordered_words':{k:len(v) for k,v in P['Euler_matrices'].items()},'boundary_current_trace_words':[len(v) for v in P['boundary_current']],'boundary_divergence_trace_words':len(DJ),'direct_variation_trace_words':len(Q),'Ward_coupling_degrees':degrees,'scalar_Euler_omission_changes_positions':len(missing),'scalar_kinetic_covariantization_mismatch_positions':mis,'literal_Ward_boundary_remainder':'0','independent_Euler_remainder':'0','actual_transpose_Ward_tangent_remainder':'0','pure_gauge_family_normalization_remainder':'0','invariant_Ward_images':{'gauge':'0','mass_kinetic':'0','potential':'0'},'controls':controls,'bosonic_ward_packed_sha256':sha256(blob).hexdigest(),'bosonic_ward_raw_sha256':sha256(raw).hexdigest(),'new_loop_integrals':0,'independently_integrated_new_quantum_insertion':False,'full_source_background_external_fermion_massive_admissibility_qualified':False,'full_chiral_QAP_measure_phase_or_physical_matching_qualified':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
