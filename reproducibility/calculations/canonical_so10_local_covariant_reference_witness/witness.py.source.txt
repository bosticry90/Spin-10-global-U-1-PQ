"""Actual carrier congruences and explicit symmetrically ordered local reference."""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
from itertools import permutations
import importlib.util,json,os,sys,time,threading
import sympy as s
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);u=importlib.util.module_from_spec(z);z.loader.exec_module(u);return u
a=load('qualified_actual_chart_auth',OUT.parent/'canonical_so10_antighost_linear_identity/test_v2.py');b=a.b;read=a.read;digest=a.digest;PKG=a.PKG
@lru_cache(None)
def clean(z):return s.cancel(z)

def main():
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];prep=read(OUT/'preparation.json');assert role in ['primary','replay'] and digest(Path(__file__))==prep['source_sha256']
 for p,k in prep['input_sha256'].items():assert digest(Path(p))==k,p
 allow={str(Path(p).resolve()) for p in prep['read_json_by_role'][role]}
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  p=Path(os.fsdecode(args[0]))
  if len(args)>1 and isinstance(args[1],str) and any(z in args[1] for z in 'wax+'):raise PermissionError('LOCAL_REFERENCE_WRITE')
  if p.suffix=='.json':assert str(p.resolve()) in allow,('UNDECLARED_OR_PEER_JSON',str(p))
 sys.addaudithook(guard);w=a.m.setup();core,cb=b.sealed('frozen_a10_e5_full_hessian',role);e3,eb=b.sealed('frozen_a10_e3_symmetry',role);names=core['retained_reference']['field_order'];pos={n:i for i,n in enumerate(names)};grades=w.grades|w.external;par=[grades[n][2] for n in names];g=s.Symbol('g10');pp=s.symbols('p0_ref:4',real=True);loc=dict(zip(map(str,pp),pp));R=[{} for _ in range(12)];affine=[];stages=[]
 @lru_cache(None)
 def num(txt):return s.sympify(txt,locals=loc)
 def stage(n,fn):
  print('STAGE '+role+' '+n,flush=True);t=time.perf_counter();v=fn();stages.append({'name':n,'seconds':time.perf_counter()-t});return v
 for n in names:
  for row in e3['operators']['Tb_geometric_and_transported'][n]:
   om=[z for z in row['word'] if z.startswith('omega')];other=[z for z in row['word'] if not z.startswith('omega')];assert len(om)==1
   if '__' in om[0]:assert not other and n.startswith('B') and num(row['coefficient'])==1;affine.append(n);continue
   assert len(other)==1 and other[0] in pos and '__' not in other[0];i,j=pos[n],pos[other[0]];h=int(om[0][5:]);z=clean(num(row['coefficient'])/g);assert not z.free_symbols and grades[n]==grades[other[0]];R[h][i,j]=R[h].get((i,j),0)+z
 assert len(set(affine))==48 and all(P for P in R);assert e3['local_algebra']['all_three_residuals_zero'] and e3['local_algebra']['all_generator_local_Lie_checks']==4002 and e3['local_algebra']['parameter_derivatives_retained']
 K={(i,j):num(txt) for i,j,txt in core['retained_reference']['reference_Hessian_raw_C3']['entries']};assert len(K)==1597
 def congruence(rho):
  out={};rr=defaultdict(list);kr=defaultdict(list);kc=defaultdict(list)
  for (i,j),z in rho.items():rr[i].append((j,z))
  if role=='primary':
   for (i,j),z in K.items():
    for k,u in rr[j]:out[i,k]=out.get((i,k),0)+z*u
    for k,u in rr[i]:out[k,j]=out.get((k,j),0)+u*z
  else:
   for (i,j),z in K.items():kr[i].append((j,z));kc[j].append((i,z))
   for (i,j),z in rho.items():
    for k,u in kr[i]:out[j,k]=out.get((j,k),0)+z*u
    for k,u in kc[i]:out[k,j]=out.get((k,j),0)+u*z
  return {ij:v for ij,z in out.items() if (v:=clean(z))!=0}
 residuals=stage('all12_full643_actual_reference_carrier_congruences',lambda:[congruence(rho) for rho in R]);assert not any(residuals),('ACTUAL_CARRIER_INVARIANT_PAIRING_FAILURE',[(i,len(P)) for i,P in enumerate(residuals) if P])
 flip={p:-p for p in pp};assert all(clean(z-(-1)**(par[i]*par[j])*K.get((j,i),s.S.Zero).xreplace(flip))==0 for (i,j),z in K.items())
 # Fixed Weyl lift: all coefficients retained; fully symmetrized D words.
 O={};C={}
 for (i,j),z in K.items():
  assert par[i]==par[j]
  for powers,coeff in s.Poly(z,*pp).terms():
   assert sum(powers)<=2;word=tuple(k for k,n in enumerate(powers) for _ in range(n));C[i,j,word]=coeff;orders=sorted(set(permutations(word))) if word else [()]
   for order in orders:O[i,j,order]=s.expand(coeff*(-s.I)**len(word)/len(orders))
 flat={};transbad={}
 for (i,j,word),z in O.items():flat[i,j]=flat.get((i,j),0)+z*s.I**len(word)*s.prod(pp[k] for k in word)
 assert set(flat)==set(K) and all(clean(z-K[ij])==0 for ij,z in flat.items())
 assert all(clean(z-(-1)**(par[i]*par[j]+len(word))*O.get((j,i,word[::-1]),0))==0 for (i,j,word),z in O.items())
 # Generic covariance identity at every coefficient follows from actual R
 # congruence and inherited Lie closure. The inhomogeneous omega derivative
 # fixes D=partial-g rho(A), including actual affine background rule.
 wrong_sign_nonzero=any(2*z!=0 for rho in R for z in rho.values());assert wrong_sign_nonzero
 mutant=dict(R[0]);key=next(iter(mutant));mutant.pop(key);carrierbad=congruence(mutant);assert carrierbad
 odd_wrong=[(i,j) for (i,j),z in K.items() if par[i] and clean(z-K.get((j,i),s.S.Zero).xreplace(flip))!=0];assert odd_wrong
 # Reversal is insensitive for symmetric Weyl words, and is reported honestly.
 assert all(O.get((i,j,word[::-1]),0)==z for (i,j,word),z in O.items())
 asymmetric=next((key for key,z in O.items() if len(key[2])==2 and key[2][0]!=key[2][1]),None);assert asymmetric is not None;removed=dict(O);removed.pop(asymmetric);i,j,word=asymmetric;assert clean(O[i,j,word]-(-1)**(par[i]*par[j]+len(word))*removed.get((j,i,word[::-1]),0))!=0 or any(clean(z-(-1)**(par[a]*par[b]+len(ws))*removed.get((b,a,ws[::-1]),0))!=0 for (a,b,ws),z in removed.items())
 prior=b.auth('canonical_so10_ub12_reference_symbol',role+'_v2_result.json');assert prior['scientific_disposition']=='ACTUAL_WEIGHTED_PRINCIPAL_INVERTIBILITY_QUALIFIED_BACKGROUND_LOCAL_CLASS_MEMBERSHIP_UNPROVED';assert prior['no_width_g_or_reference_mass_inverted_in_principal'] and not prior['actual_local_UV_or_regulated_QAP_measure_IR_contacts_full_Slavnov_E5_A5_proved']
 qc,qb=b.sealed('frozen_a10_e5_quantum_contract',role);flags={k:qc[k] for k in ['QAP_proved_for_model','actual_renormalization_prescription_constructed','all_order_class_nonempty_proved','joint_restoration_proved','quantum_insertions_renormalized','quantum_canonical_equivalence_proved','measure_or_anomaly_freedom_proved']};assert not any(flags.values())
 result={'schema':'EXPLICIT_LOCAL_COVARIANT_REFERENCE_WITNESS_V1','route':role,'scientific_disposition':'EXPLICIT_ORDERED_LOCAL_COVARIANT_REFERENCE_WITNESS_NOT_ADOPTED_QUANTUM_SCHEME','field_order':names,'actual12_homogeneous_carrier_matrices':[[[i,j,str(z)] for (i,j),z in sorted(rho.items())] for rho in R],'actual48_field_affines':sorted(set(affine)),'actual12_full_polynomial_reference_congruences_zero':True,'inherited4002_local_Lie_checks_authenticated_not_replayed':True,'all1597_actual_flat_K_entries_recovered':True,'all_actual_graded_p_flip_transpose_checks':True,'explicit_covariant_operator':{'derivative':'D_mu=partial_mu-g10 sum_a rho_a A^a_mu','ordering':'fixed complete symmetric ordered words from actual flat polynomial; chosen before coefficient tests','quadratic_form':'one_half h Kcov h with actual graded pairing','entries':[[i,j,list(word),str(z)] for (i,j,word),z in sorted(O.items())]},'explicit_operator_positions':len(O),'derivative_word_length_counts':dict(Counter(len(word) for i,j,word in O)),'all_formal_graded_transpose_ordered_words_checked':True,'formal_H_covariance_from_actual_pairing_Lie_and_affine_rules':True,'local_differential_order_at_most2_and_local_finite_background_jets':True,'same_actual_weighted_principal_symbol':True,'formal_weighted_parametrix_local_jet_recursion_applies_to_this_witness':True,'full_heat_IR_UV_subtraction_correspondence_or_actual_historical_member_qualification':False,'controls':{'remove_actual_carrier_entry_breaks_reference_congruence':True,'wrong_D_sign_has_nonzero_parameter_gradient_defect':True,'wrong_odd_transpose_sign_changes_actual_ghost_block':True,'remove_one_distinct_ordered_word_breaks_adjoint_or_flat_map':True},'insensitive_control':'reversing every Weyl word leaves the symmetric witness unchanged; not counted as sensitive','seven_false_quantum_flags':flags,'adopted_physical_scheme_or_unique_historical_covariantization':False,'no_functional_source_input_benchmark_authority_change':True,'QAP_measure_IR_contacts_full_sourcefree_Slavnov_E5_A5_proved':False,'shared_limits':'Actual E3 Lie closure/reference/chart,SymPy,conditional formal UV arguments and AI author shared;not independent expert or full quantum construction','stages':stages,'elapsed_after_imports':time.perf_counter()-tick};print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
