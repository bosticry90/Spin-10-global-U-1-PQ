"""BSR1 independent finite coordinate reconstruction and scoped receipt review."""
from data import *
start=begin('replay');old=read(ROOT/OLD_POINT);base=read(CAL/'canonical_so10_scalar_benchmark/STAGE1_POINT.json')['free_coefficients']
oldvals={n:F(old['changed_free_coefficients'][n] if n in old['changed_free_coefficients'] else base[n]) for n in NAMES}
p=read(ROOT/FINITE_POINT);p1,p2,xSigma,s,z,D,t,delta,e=[F(p[n]) for n in ['p1','p2','x','s','z','D','t','Delta','eta']]
newvals=[p1,p2,delta+t/4,t,xSigma/8,(5*s+z)/2-5*D/24,(-3*s-z)/2+5*D/24,(z-s)/4]
contract=(CAL/'canonical_so10_direct_two_loop_gauge_scalar_threshold/RECORD.md').read_text(encoding='utf-8');assert 'frozen canonical' in contract and 'positive-Higgs benchmark' in contract
assert old['inherits']=='../canonical_so10_scalar_benchmark/STAGE1_POINT.json'
r={label:read(CAL/folder/name) for label,(folder,name) in RECEIPTS.items()}
assert r['search']['scientific_disposition']=='INCONCLUSIVE_FULL_EIGHT_QUARTIC_DOMAIN'
assert r['eta_exclusion']['fixed_input_eight_quartic_tree_screen_excluded'] and r['eta_exclusion']['physical_eta']=='3/10'
assert r['finite_contact']['complete_contact_perturbativity_pass'] and not r['finite_contact']['quantum_control_proved'] and not r['finite_contact']['new_benchmark_adopted']
assert r['finite_BFB']['same_frozen_point'] and not r['finite_BFB']['quantum_control_proved'] and not r['finite_BFB']['new_benchmark_adopted']
finish('replay',{'schema':'BSR1','old_point_sha256':digest(ROOT/OLD_POINT),'finite_point_sha256':digest(ROOT/FINITE_POINT),
 'old_quartics':{n:str(v) for n,v in oldvals.items()},'finite_quartics':{n:str(v) for n,v in zip(NAMES,newvals)},
 'old_eta':str(F(old['changed_free_coefficients']['zEta:re'])),'finite_eta':str(e),'receipt_statuses':{k:v['status'] for k,v in r.items()},
 'C1_contract_selects_positive_higgs':True,'xSigma_not_gauge_x':True,'finite_classical_certificates_do_not_establish_quantum_control':True,
 'stale_domain_recommendation_requires_correction':True,'old_numerical_results_reinterpreted_as_finite_point':False,'new_physics_or_benchmark_adopted':False},start)
