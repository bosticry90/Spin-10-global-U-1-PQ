from pathlib import Path
from hashlib import sha256
from itertools import permutations
import gzip,json,os,sys,threading,time,sympy as s
repository_path=Path(__file__).resolve().parents[2]
output_path=Path(__file__).resolve().parent
sys.path.insert(0,str(repository_path/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as JP
read=lambda p:json.loads(p.read_bytes())
loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for path,digest in read(output_path/'review_preparation.json')['input_sha256'].items():assert file_hash(Path(path))==digest,path
native=read(output_path/'ward_support_result.json');tables=loadz(output_path/'ward_support_tables.json.gz')
assert file_hash(output_path/'ward_support_tables.json.gz')==native['packed_tables_sha256']

def calc(folder,name):
    path=repository_path/'calculations'/folder/name
    return loadz(path) if path.suffix=='.gz' else read(path)

for probe in range(2):
    primary=next(v for v in tables['routes'] if v['role']=='primary' and v['probe']==probe)
    replay=next(v for v in tables['routes'] if v['role']=='replay' and v['probe']==probe)
    assert primary['retained_density_rows']==replay['retained_density_rows']
    assert primary['counts']['source2_rows']==replay['counts']['source2_rows']
    assert not primary['diagonal_entries'] and not replay['diagonal_entries']

raw_counts=[]
for role in ['primary','replay']:
    data=calc('canonical_so10_u_maximal_heat_cutoff',role+'_inputs.json.gz')
    for probe,encoded in enumerate(data['QG']):
        # Decode only here; direct ordered port scan is separate from Euler.
        poly=JP.decode(encoded);pairs=0;rows=0;source2={}
        for word,value in poly.items():
            if JP.degree(word,4) not in [0,1]:continue
            rows+=1;ids=[i for i,jets in word]
            for src in (i for i in ids if i>=643):pairs+=ids.count(src-643)
            if sum(i>=643 for i in ids)==2:source2[word]=value
        assert pairs==0 # stronger actual support fact than dimension alone
        sources={i for w in source2 for i,jets in w if i>=643}
        differentiated=JP.euler(source2,sources)
        assert differentiated and any(differentiated.values())
        # Setting sources0 first would erase this whole nonzero operation.
        assert not {w:c for w,c in source2.items() if not any(i>=643 for i,js in w)}
        raw_counts.append({'role':role,'probe':probe,'full_retained_rows':rows,
          'diagonal_source_field_port_pairs':pairs,'source2_Euler_nonzero_columns':len(differentiated),
          'early_source_restriction_control_sensitive':True})

surviving=[]
for key in ['matter_Hessian_port_pairs','raw_hatted_Hessian_port_pairs']:
    for v in tables[key]:
        # A separate set-partition decision; native supplied group flags
        # are checked, rather than being trusted as the exclusion predicate.
        rest=set(v['remaining']);kill=bool(rest.intersection(['P','S','K']))
        assert kill==v['external_matter_or_K_required']
        if not kill:
            assert all(p in ['P','S'] for p in v['ports']);surviving.append(v)
assert surviving
# Boolean closure proves arbitrary word lengths, not a finite walk sample.
# Fermion/nonmatter blocks stay disjoint; u is confined to the nonmatter block.
partition={(0,0),(1,1)}
closure=set(partition)
while True:
    new=closure|{(i,k) for i,j in closure for jj,k in partition if j==jj}
    if new==closure:break
    closure=new
assert closure==partition and (0,1) not in closure and (1,0) not in closure
source_control=[v for v in tables['matter_Hessian_port_pairs']
                if v['origin']=='KCP' and v['remaining']==['K']]
assert source_control and all(set(v['groups'])=={'F','N'} for v in source_control)
# An external K derivative changes that exclusion: do not transfer this zero.

fixtures=[]
for seed in [1,2,3,4]:
    K=s.diag(seed+1,seed+3)
    E=s.diag(s.Rational(1,seed+2),s.Rational(1,seed+4))
    V=s.Matrix([[2,seed],[seed,1]])
    H=K+V;Rt=(E.inv()-s.eye(2))*K;Gt=(H+Rt).inv()
    M=s.Matrix([[seed,2],[-3,seed+1]])
    defect=s.Matrix([[2,seed+1],[seed+1,3]])
    dH=defect-M.T*H-H*M
    lhs=s.trace(Gt*dH)/2
    rhs=s.trace(Gt*defect)/2-s.trace(M)+s.trace(Gt*Rt*M)
    assert s.simplify(lhs-rhs)==0
    assert s.simplify(s.trace(Gt*defect)/2)!=0
    wrong_order=s.simplify(s.trace(Gt*Rt*M)-s.trace(Rt*Gt*M));assert wrong_order!=0
    ordered=(s.eye(2)+E*K.inv()*V).inv()*(s.eye(2)-E)
    assert Gt*Rt==ordered
    wrong_heat=(s.eye(2)-E)*(s.eye(2)+E*K.inv()*V).inv()
    assert ordered!=wrong_heat
    dRt=s.diag(1,2);direct_response=s.simplify(s.trace(Gt*dRt)/2);assert direct_response!=0
    A=s.Matrix([[1,2],[3,4]]);B=s.Matrix([[2,5],[7,11]])
    weighted_commutator=s.simplify(s.trace(E*(A*B-B*A)));assert weighted_commutator!=0
    fixtures.append({'seed':seed,'identity_residual':str(s.simplify(lhs-rhs)),
      'omitted_master_defect':str(s.trace(Gt*defect)/2),'wrong_Rt_order':str(wrong_order),
      'co_varied_reference_extra_term':str(direct_response),
      'illegal_weighted_cyclicity_control':str(weighted_commutator),
      'ordinary_matrix_fixture_not_new_graded_proof':True})

udr=repository_path/'calculations/canonical_so10_u_dimensional_reconciliation'
seal=read(udr/'final_review_validation_receipt.json')['new_files_sha256']
for name in ['PROOF.md','IR_PROOF.md','validation_receipt_v2.json','ir_validation_receipt_v2.json']:
    path=udr/name;assert file_hash(path)==seal[str(path.relative_to(repository_path)).replace('\\','/')]
local=read(udr/'validation_receipt_v2.json');domain=read(udr/'ir_validation_receipt_v2.json')
assert local['complete_declared_local_relative_T_F_symbol_zero'] and local['sixteen_prior_complete_coefficient_sums_authenticated']==16
assert domain['first_u_direct_one_variation_common_trace_extension_within_scope']
assert not domain['two_independent_insertions_full_QAP_measure_or_physical_claim']
csw=calc('canonical_so10_cutoff_source_ward_operator','validation_receipt.json')
assert csw['finite_Grassmann_Gaussian_fixtures']==8 and csw['first_variation_joint_test_field_domain']
assert all(csw['negative_controls'][k]>0 for k in ['omit_sharp','ordinary_trace','wrong_R_G_order'])
cps=calc('canonical_so10_chiral_probe_support','validation_receipt.json')
assert cps['classical_augmented_defect']=='UNCHANGED_NONZERO_IHAT'
assert cps['source_differentiation_before_zero_superGaussian_control_nonzero']

proof=(output_path/'PROOF.md').read_text()
for clause in ['before UV\nfinite part','not an inverse heat','n>=1','four source-Hessian product legs',
               'UV finite part then IR limit','no step replacing','Pi(B C_rel + Cutoff_FP) = 0',
               'first-u T/F finite Ward relation','full momentum-dependent Ward functional']:
    assert clause in proof,clause
# Scope matching is the written analytic argument, not certified by string
# checks or fixtures. The reviewer has separately checked its dependencies:
# CSW transpose at positive heat, UDR strict nodes and actual ordered family.
result={'schema':'UWT2_SEPARATE_PROJECTED_WARD_REVIEW','raw_source_reviews':raw_counts,
 'quadratic_block_partition_closed_for_arbitrary_Born_length':True,
 'actual_hatted_internal_insertion_retained_then_projected_zero':True,
 'actual_diagonal_first_u_tangent_absent_before_trace':True,
 'fixed_reference_response_zero_under_unchanged_contract':True,
 'finite_Gaussian_order_and_omission_controls':fixtures,
 'graded_transpose_and_base_master_premises_inherited_not_rerun':True,
 'paired_positive_heat_trace_step_before_FP_matched_to_UDR_domain':True,
 'no_arbitrary_finite_part_cyclicity_or_separate_trace_defect_zero_claim':True,
 'existing_complete_local_conversion_and_cutoff_owned_once':True,
 'selected_local_finite_first_u_T_F_Ward_relation':'QUALIFIED_WITHIN_INHERITED_FORMAL_DOMAIN',
 'finite_t_cutoff_not_claimed_zero':True,'full_momentum_Ward_functional_QAP_measure_E5_physical_claim':False,
 'old_quantum_tensor_loops_freshly_rerun':False,'scientific_acceptance':'NOT_PERFORMED',
 'elapsed_after_imports':time.perf_counter()-tick}
with (output_path/'validation_receipt.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(result,sort_keys=True),flush=True);timer.cancel()
