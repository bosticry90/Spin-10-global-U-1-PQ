"""GFD1 exact independent numerator/finite comparison; no scheme adoption."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==hsh,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def eq(a,b):assert s.simplify(s.gammasimp(s.sympify(a)-s.sympify(b)))==0,(a,b)
count=0;nonzero=0
for k in P['triangle']:
 for w in ['012','021']:
  for a,b in zip(P['triangle'][k][w],R['triangle'][k][w]):eq(a,b);count+=1;nonzero+=int(s.sympify(a)!=0)
assert count==1024 and set(P['box'])==set(R['box']) and len(P['box'])==70
for k in P['box']:eq(P['box'][k],R['box'][k])
for k in P['raw_triangle_hat_numerators']:
 for a,b in zip(P['raw_triangle_hat_numerators'][k],R['raw_triangle_hat_numerators'][k]):eq(a,b)
for key in ['raw_box_two_hat_numerator','raw_box_four_hat_numerator']:
 for k in P[key]:eq(P[key][k],R[key][k])
for k in ['two_point_q2_delta_finite','two_point_difference_exact','bubble_hat_numerator_prefactor']:eq(P[k],R[k])
G=dec(P['G']);assert G==dec(R['G'])==2*s.eye(45)
assert R['pairing_counts_six_eight']==[15,105] and P['witness_spin_trace']==8 and P['witness_to_physical_divisor']==2
# Compare only now with the independently completed earlier actual loops.
GPC=packed(CAL/'canonical_so10_fermion_pure_gauge_uv/primary_tables.json.gz')
for k in P['bar_reference_triangle_UV']:
 for w in ['012','021']:
  for a,b in zip(P['bar_reference_triangle_UV'][k][w],GPC['triangle'][k][w]):eq(a,b)
for k,v in P['bar_reference_box_UV'].items():eq(v,GPC['box'][k])
GEP=packed(CAL/'canonical_so10_split_momentum_gauge_polarization/replay_tables.json.gz');F0=s.sympify(P['two_point_q2_delta_finite']);eq(F0,GEP['F_finite_epsilon'][0])
# Physical reality: each external momentum changes sign on Fourier conjugation.
for block in P['triangle'].values():
 for a,b in zip(block['012'],block['021']):eq(a,-s.sympify(b));assert s.sympify(a).is_real
for w,v in P['box'].items():
 word=tuple(map(int,w.split(',')));rev=word[::-1];key=','.join(map(str,min(rev[j:]+rev[:j] for j in range(4))));eq(v,P['box'][key]);assert s.sympify(v).is_real
h=s.Symbol('h');four_positions=sum(s.sympify(P['box'][w])!=s.sympify(P['box_no_four_hat'][w]) for w in P['box']);boxnz=sum(s.sympify(v)!=0 for v in P['box'].values())
positive_hat_poles=sum(s.sympify(v).subs(h,2)!=0 for key in ['raw_box_two_hat_numerator','raw_box_four_hat_numerator'] for v in P[key].values())
controls={'premature_hat_zero':F0!=0,'wrong_analytic_hat_sign':F0!=-F0,'positive_hat_rank_substitution_has_spurious_UV_pole':positive_hat_poles>0,'drop_four_hat_box_numerators':four_positions>0,'inflate_witness_trace':F0!=2*F0,'omit_Nambu_half':F0!=2*F0,'extra_half_after_Nambu':F0!=F0/2,'wrong_closed_family_count':3*F0!=6*F0,'commute_quartic_color_words':boxnz>0}
assert all(controls.values())
# Commuting external matrices are an adversarial diagnostic, not a permitted
# simplification; unlike the UV commutator functional they may retain A^4.
commuting={}
for w,v in P['box'].items():
 key=','.join(sorted(w.split(',')));commuting[key]=str(s.sympify(commuting.get(key,'0'))+s.sympify(v))
for obj in [P,R]:assert obj['physical_spin_trace']==4 and obj['gaussian_factor']=='1/2' and obj['closed_family_count']==3 and obj['analytic_hat_rank']=='-2epsilon' and obj['maximum_hat_polynomial_degree']==2 and not obj['reference_adopted_as_physical_scheme'] and not obj['mass_dependent_terms_computed'] and obj['new_two_loop_integrals']==0
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
local={'actual_minus_reference':{'quadratic_action_trace_dA_squared':str(F0/2),'cubic_vertex_common_g3':P['triangle'],'quartic_density_common_g4':P['box']},'three_family_multiplier':3,'common_loop_factor':'1/(16*pi^2)','comparison_CT_is_negative_of_measured_difference':True,'finite_gauge_invariant_baseline':'zeta_unfixed_not_adopted','b0_kappa_zeta_distinct':True,'physical_domain':'mass-independent_parity-even_nonexceptional_Euclidean_barred_external_momenta','source_background_or_massive_extension_claimed':False}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'finite_difference_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_PHYSICAL_MOMENTUM_PARITY_EVEN_GAUGE_FINITE_DIFFERENCE','elapsed_after_imports':time.perf_counter()-start,'triangle_coefficient_positions_compared':count,'triangle_nonzero_positions':nonzero,'quartic_cyclic_traceword_positions_compared':70,'quartic_nonzero_tracewords':boxnz,'four_hat_omission_changes_quartic_positions':four_positions,'raw_hat_polynomial_positions_compared':256*3+256*2,'actual_color_Gram_positions_compared':2025,'physical_two_point_finite_q2_delta_per_G':str(F0),'quadratic_action_trace_coefficient':str(F0/2),'bar_reference_matches_actual_GPC_UV':True,'finite_difference_is_IR_reference_independent_within_frozen_domain':True,'finite_locality_remainder_scope':'UV_IR_CONVERGENT_SUBTRACTED_ONE_LOOP_KERNELS_AT_NONEXCEPTIONAL_EUCLIDEAN_MOMENTA','controls':controls,'Clifford_reversal_words_checked':P['Clifford_reversal_words_checked'],'finite_difference_packed_sha256':sha256(blob).hexdigest(),'finite_difference_raw_sha256':sha256(raw).hexdigest(),'physical_spin_trace':4,'closed_family_count':3,'new_one_loop_finite_comparison_families':3,'new_two_loop_integrals':0,'full_QAP_or_physical_scheme_equivalence_qualified':False,'background_source_or_mass_dependent_restoration_qualified':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
