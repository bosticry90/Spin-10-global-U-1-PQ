from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import permutations
import gzip,json,os,re,threading,time,sympy as s
O=Path(__file__).resolve().parent;R=O.parents[1]
tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
read=lambda p:json.loads(p.read_bytes());loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()));H=lambda p:sha256(p.read_bytes()).hexdigest()
for pp,h in read(O/'preparation.json')['input_sha256'].items():assert H(Path(pp))==h,pp
def calc(folder,name):
    p=R/'calculations'/folder/name;return loadz(p) if p.suffix=='.gz' else read(p)
def truth(folder,name,key):
    z=calc(folder,name);assert z[key] is True,(folder,name,key);return {'file':'calculations/'+folder+'/'+name,'predicate':key,'sha256':H(R/'calculations'/folder/name)}
facts=[]
for args in [
 ('canonical_so10_intrinsic_auxiliary_source','kernel_validation_receipt.json','D_jet_zero_supported_not_assumed'),
 ('canonical_so10_intrinsic_auxiliary_ghost_source','kernel_primary_tables.json.gz','longitudinal_no_closed_vector_spectator'),
 ('canonical_so10_intrinsic_quadratic_source_contacts','kernel_validation_receipt_v2.json','zero_D_jet_from_longitudinal_support_not_interpolation'),
 ('canonical_so10_remaining_u_contact_vertices','validation_receipt.json','fixed_Djet0_structural_for_declared_contacts'),
 ('canonical_so10_unprobed_antighost_kernel','universal_validation_receipt.json','fixed_Djet0_structural'),
 ('canonical_so10_unprobed_auxiliary_source_kernel','universal_validation_receipt.json','fixed_D_jet_zero_structural_not_interpolated'),
 ('canonical_so10_unprobed_source_root_module','kernel_primary_tables.json.gz','fixed_Djet0_by_longitudinal_endpoints'),
 ('canonical_so10_unprobed_marginal_C3','primary_blocks.json.gz','no_free_D_trace_by_pinned_connectors_and_metric_V2'),
 ('canonical_so10_unprobed_marginal_C3','replay_blocks.json.gz','all_four_component_Lorentz_monomials_verified'),
 ('canonical_so10_unprobed_baseline_C2','kernel_primary_tables.json.gz','all_actual_marginal_C2_paths_are_ghost_only'),
 ('canonical_so10_unprobed_baseline_C2','kernel_replay_tables.json.gz','all_actual_marginal_C2_paths_are_ghost_only'),
 ('canonical_so10_u_lower_cutoff_contraction','lorentz_result.json','all_four_component_polynomial_shapes_verified'),
 ('canonical_so10_u_F_fourth_support','review_result.json','all_label_tables_equal')]:facts.append(truth(*args))
lor=calc('canonical_so10_u_lower_cutoff_contraction','lorentz_result.json')
assert lor['all_label_input_entries']==286804 and all(z['no_unpinned_vector_only_cycle'] for z in lor['path_domain'])
for folder,name,anchor in [
 ('canonical_so10_intrinsic_correlated_source_contacts','CONTACT_DERIVATION.md','There is no\nclosed vector spectator'),
 ('canonical_so10_u_F_fourth_support','PROOF.md','Every nontrivial vector chain is longitudinally pinned'),
 ('canonical_so10_unprobed_log3_support','RESULT.md','same qualified\nACV J/W pin theorem applies'),
 ('canonical_so10_full_jet_source_master_bridge','PROOF.md','including two fluctuation legs')]:
    pp=R/'calculations'/folder/name;assert anchor in pp.read_text(),(folder,name,anchor)
    facts.append({'file':str(pp.relative_to(R)).replace('\\','/'),'analytic_scope_anchor':anchor,'sha256':H(pp),'old_calculation_freshly_replayed':False})

# Source-class closure is checked on the actual nonminimal map and
# scalar rules,not inferred from a selected zero coefficient.
d=calc('canonical_so10_intrinsic_full_source_descent','variation_primary_inputs.json.gz');maps=d['maps'];source_entries=0
for out,rows in maps['source_maps']:
    assert 0<=out<90
    for word,value in rows:
        assert all(0<=i<90 or 135<=i<180 for i in word);source_entries+=1
r=calc('canonical_so10_intrinsic_full_source_descent','variation_replay_inputs.json.gz');qx_rows=0
for out,rows in r['source_Qx'].items():
    for row in rows:
        assert len(row['word'])==2 and sum(n.startswith('C') for n in row['word'])==1 and sum(n.startswith('x_') for n in row['word'])==1;qx_rows+=1
assert qx_rows==29754
for row in d['assembly']['outputs']:
    assert set(row['formal_basis'])=={'chi4','log2','log3','log5'}
    for basis,z in row['formal_basis'].items():assert set(z)=={'rho_Jx','u_Jx_C','rho_JLambda_x','u_Ja_x','u_JLambda_C_x'}

u=calc('canonical_so10_u_operation_root_inventory','root_primary_tables.json.gz');roots=set();flow_counts=Counter();tokens=set()
for probe,row in enumerate(u['results']):
    for target,ops in row['targets'].items():
        for pat,nu,count in ops['nonzero_flows_by_root']:roots.add((tuple(pat),nu))
        for pat,nu,out,rem,value in ops['aggregate_flows']:
            ids=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',value));assert ids<={'g10','xi','eta_H','sqrt','I'},(value,ids);tokens|=ids;flow_counts[probe,target]+=1
assert len(roots)==10
fixed_roots={
 (('C','C','JL','JL'),0):'UMC full pin/C3/C4;UBC C2 ghost-only',
 (('C','C','JL','a'),0):'UMC full pin/C3/C4;UBC C2 ghost-only',
 (('C','JL','Ja'),0):'ICR pinned linear ghost-mass specialization',
 (('C','JL','x'),1):'UAK whole pin proof',
 (('C','Ja','a'),0):'UBC C2 ghost-only;ULS qualified AAK pin specialization',
 (('C','Jx','x'),0):'USR longitudinal source/kinetic endpoints',
 (('C','a','x'),1):'AAK complete466 profile pin proof',
 (('Ja','Ja'),0):'IQC block zero before trace',
 (('Ja','x'),1):'IQC block zero before trace',
 (('L','x'),1):'IQC ordinary auxiliary pinned/ghost families'}
assert roots==set(fixed_roots)

# Exact projector algebra with noncommuting color matrices. Pair (A,B)
# denotes I_L tensor A+P tensor B,without commuting A through any B.
D,ep=s.symbols('D epsilon');I=s.eye(2);Z=s.zeros(2)
def mul(X,Y):
    a,b=X;c,d=Y;return (a*c,a*d+b*c+b*d)
def trace(X):return s.expand(D*s.trace(X[0])+s.trace(X[1]))
fixtures=[]
mats=[s.Matrix([[1,2],[3,5]]),s.Matrix([[7,11],[13,17]]),s.Matrix([[19,23],[29,31]])]
assert mats[0]*mats[1]!=mats[1]*mats[0]
for order in permutations(range(3)):
    X=(Z,I)
    for at in order:X=mul(X,(mats[at],mats[(at+1)%3]))
    value=trace(X);assert s.diff(value,D)==0 and X[0]==Z
    fixtures.append({'ordered_colors':list(order),'trace':str(value),'dimension_jet':str(s.diff(value,D))})
wrong=trace((mats[0],Z));assert s.diff(wrong,D)!=0
evanescent=s.expand((D-4)*s.trace(mats[0])/ep).subs(D,4-2*ep);assert s.simplify(evanescent)==-12

def owned(folder,name):
    pp=R/'calculations'/folder/name;rel=str(pp.relative_to(R)).replace('\\','/')
    assert H(pp)==calc(folder,'final_review_validation_receipt.json')['new_files_sha256'][rel]
    return loadz(pp)
prior={};zero_files=[]
for folder,name,basis,only in [
 ('canonical_so10_unprobed_baseline_C2','baseline_complete_comparison_v2.json.gz','chi4',None),
 ('canonical_so10_unprobed_log2_completion','log2_complete_comparison.json.gz','log2',None),
 ('canonical_so10_unprobed_log3_support','T_log3_complete_comparison_v2.json.gz','log3','T'),
 ('canonical_so10_unprobed_marginal_C3','F_log3_complete_comparison.json.gz','log3','F')]:
    z=owned(folder,name)
    for row in z['tensors']:
        target=only or row['target'];assert not row['sum'];prior[basis,row['probe'],target]=True
    zero_files.append({'file':'calculations/'+folder+'/'+name,'sha256':H(R/'calculations'/folder/name),'old_loop_freshly_replayed':False})
for folder,name,target in [('canonical_so10_u_T_cutoff_tensor','late_remainders_v2.json.gz','T'),('canonical_so10_u_F_remaining_contraction','late_remainders.json.gz','F')]:
    z=owned(folder,name)
    for row in z:assert not row['remainders'];prior['log5',row['probe'],target]=True
    zero_files.append({'file':'calculations/'+folder+'/'+name,'sha256':H(R/'calculations'/folder/name),'old_loop_freshly_replayed':False})
assert set(prior)=={(b,p,t) for b in ['chi4','log2','log3','log5'] for p in range(2) for t in ['T','F']}
out={'schema':'UDR1_DIMENSIONAL_INPUT_RECONCILIATION','imported_pin_and_shape_facts':facts,
 'homogeneous_nonminimal_source_map_entries':source_entries,'scalar_Qx_source_rows_checked':qx_rows,'Jx_source_class_cannot_mix_into_T_F':True,
 'all_ten_native_roots_matched':[{'types':list(p),'intrinsic_degree':nu,'fixed_jet_proof':fixed_roots[p,nu]} for p,nu in sorted(roots)],
 'actual_UOR_flow_counts':[[list(k),v] for k,v in sorted(flow_counts.items())],'operation_coefficient_symbols':sorted(tokens),'operation_has_no_D_parameter':True,
 'noncommuting_projector_fixtures':fixtures,'unpinned_spectator_dimension_jet':str(s.diff(wrong,D)),'evanescent_times_pole_finite_control':str(evanescent),
 'fixed_dimensional_contribution_by_stage':{k:0 for k in ['homogeneous_C1','quadratic_source_Euler','native_Bu_C0','ordered_cutoff']},
 'qualified_zero_tables':zero_files,'complete_formal_T_F_symbol_zero_both_probes':True,'full_continuum_Ward_QAP_or_E5_claim':False,
 'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with (O/'audit_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
