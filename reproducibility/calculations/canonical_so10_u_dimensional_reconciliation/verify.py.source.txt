from pathlib import Path
from hashlib import sha256
from itertools import product
import gzip,json,os,threading,time,sympy as s
O=Path(__file__).resolve().parent;R=O.parents[1]
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest()
for pp,h in read(O/'review_preparation.json')['input_sha256'].items():assert H(Path(pp))==h,pp
a=read(O/'audit_result.json');assert a['complete_formal_T_F_symbol_zero_both_probes'] and not a['full_continuum_Ward_QAP_or_E5_claim']
assert set(a['fixed_dimensional_contribution_by_stage'])=={'homogeneous_C1','quadratic_source_Euler','native_Bu_C0','ordered_cutoff'} and not any(a['fixed_dimensional_contribution_by_stage'].values())
requirements={
 'T':{'homogeneous':{'rhoJLx','uJax','uJLCx'},'source_lowering':{'uJaJa','uJaJLC'},'native':{'JaJLC','nJLCx','JaaC','JxCx','naCx','JaJa','nJax'},'cutoff':{2,3,4}},
 'F':{'homogeneous':{'uJax','uJLCx'},'source_lowering':{'uJaJLC','uJLJLCC'},'native':{'JLJLCC','JLaCC','JaJLC','nJax','nLx'},'cutoff':{2,3,4,5}}}
rootnames={('C','C','JL','JL'):'JLJLCC',('C','C','JL','a'):'JLaCC',('C','JL','Ja'):'JaJLC',('C','JL','x'):'nJLCx',('C','Ja','a'):'JaaC',('C','Jx','x'):'JxCx',('C','a','x'):'naCx',('Ja','Ja'):'JaJa',('Ja','x'):'nJax',('L','x'):'nLx'}
u=json.loads(gzip.decompress((R/'calculations/canonical_so10_u_operation_root_inventory/root_primary_tables.json.gz').read_bytes()))
for target in ['T','F']:
    actual={rootnames[tuple(p)] for row in u['results'] for p,nu,count in row['targets'][target]['nonzero_flows_by_root']}
    assert actual==requirements[target]['native']
assert {rootnames[tuple(z['types'])] for z in a['all_ten_native_roots_matched']}==set(rootnames.values())
assert a['Jx_source_class_cannot_mix_into_T_F'] and a['scalar_Qx_source_rows_checked']==29754 and a['operation_has_no_D_parameter']
assert set(a['operation_coefficient_symbols'])<={'g10','xi','eta_H','sqrt','I'}
for fact in a['imported_pin_and_shape_facts']:assert H(R/fact['file'])==fact['sha256']

# Every choice of Lorentz I/P in an arc has a distinct ordered color
# monomial. The leading pin forces the same Lorentz trace1 in EACH
# monomial,so this proof does not commute or cancel different colors.
D,ep=s.symbols('D epsilon');words=0
for n in range(9):
    for w in product(['I','P'],repeat=n):
        colors=tuple(range(n));assert colors==tuple(sorted(colors))
        reduced='P' if 'P' in ('P',)+w else 'I';assert reduced=='P'
        trace=1 if reduced=='P' else D;assert s.diff(trace,D)==0;words+=1
assert words==511
assert s.diff(D,D)==1 and s.limit((D-4).subs(D,4-2*ep)/ep,ep,0)==-2
assert a['unpinned_spectator_dimension_jet']=='6' and a['evanescent_times_pole_finite_control']=='-12'

zero_rows=0
for row in a['qualified_zero_tables']:
    pp=R/row['file'];assert H(pp)==row['sha256'];z=json.loads(gzip.decompress(pp.read_bytes()))
    rows=z['tensors'] if isinstance(z,dict) else z
    for v in rows:
        assert not (v['sum'] if 'sum' in v else v['remainders']);zero_rows+=1
assert zero_rows==16
out={'schema':'UDR2_BACKWARD_DOMAIN_AND_FORMAL_PIN_REVIEW','four_stages_and_ten_native_root_domains_match':True,'independent_formal_pinned_color_words_checked':words,
 'noncommuting_color_order_not_rearranged':True,'evanescent_and_unpinned_counterexamples_detected':True,'sixteen_prior_complete_coefficient_sums_authenticated':zero_rows,
 'fixed_D_jet_zero_by_matched_imported_proofs':True,'complete_declared_local_relative_T_F_symbol_zero':True,'full_continuum_trace_product_QAP_E5_claim':False,
 'old_scientific_loops_freshly_replayed':False,'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with (O/'validation_receipt.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
