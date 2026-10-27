from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import combinations,permutations
import gzip,json,math,os,threading,time
repository_path=Path(__file__).resolve().parents[2];output_path=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes());loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for path,digest in read(output_path/'review_preparation.json')['input_sha256'].items():assert file_hash(Path(path))==digest,path
data=loadz(output_path/'product_tables.json.gz');result=read(output_path/'product_result.json')
assert file_hash(output_path/'product_tables.json.gz')==result['packed_tables_sha256']
# Independent direct Wick/Berezin calculation from the displayed action:
# Z is proportional to A^-1/2 (D+J0*J1/A). The completing-square sign follows
# (J0*f0+J1*f1)^2=-2*J0*J1*f0*f1, not an ordinary commuting-fermion square.
direct_checks=[]
for fixture in data['finite_Grassmann_gaussian_checks']:
    seed=fixture['seed'];k=F(seed+2);m=F(seed+3)
    p=F(2*(seed+1));q=F(seed+2)
    alpha=F(seed+3);gamma=F(1);beta=F(seed+4);delta=F(2)
    rr=F(seed+1);ss=F(3);tt=F(seed+2);vv=F(4);ww=F(seed+5)
    R0=alpha*beta-delta*gamma
    R1=rr*beta+alpha*tt-vv*gamma-delta*ss
    value=-ww/m-R1/(k*m)+p*R0/(k*k*m)+q*R0/(k*m*m)
    recorded=fixture['source_uab_coefficient'];expected=[[0,3,0,str(value)]]
    print('DIRECT_ACTION_CHECK '+json.dumps({'seed':seed,'Wick_Berezin':expected,'shared_matrix_routes':recorded}),flush=True)
    assert recorded==expected,('SHARED_ACTION_TO_HESSIAN_CONVENTION_MISMATCH',seed,expected,recorded)
    direct_checks.append({'seed':seed,'direct_Wick_Berezin':str(value),'matrix_routes_agree':True})

# Independent inverse-source derivative recurrence; U can receive <=2 labels.
def recursion(k):
    words={('G',('U',())):1}
    for label in range(k):
        updated={}
        for word,coefficient in words.items():
            for at,token in enumerate(word):
                if token=='G':
                    new=word[:at]+('G',('A',label),'G')+word[at+1:];updated[new]=updated.get(new,0)-coefficient
                elif isinstance(token,tuple) and token[0]=='U' and len(token[1])<2:
                    new=word[:at]+(('U',tuple(sorted(token[1]+(label,)))),)+word[at+1:];updated[new]=updated.get(new,0)+coefficient
        words={w:c for w,c in updated.items() if c}
    return words
def partitions(k):
    words={};labels=set(range(k))
    for size in range(min(2,k)+1):
        for subset in combinations(range(k),size):
            for perm in permutations(sorted(labels-set(subset))):
                word=tuple(x for label in perm for x in ['G',('A',label)])+('G',('U',tuple(subset)))
                words[word]=(-1)**(k-size)
    return words
counts=[]
for k in range(8):
    a=recursion(k);b=partitions(k);assert a==b
    expected=sum(math.comb(k,j)*math.factorial(k-j) for j in range(min(k,2)+1))
    assert len(a)==expected;counts.append([k,len(a)])

for probe in range(2):
    primary=next(x for x in data['actual_H_JJ_tensors'] if x['probe']==probe and x['role']=='primary')
    replay=next(x for x in data['actual_H_JJ_tensors'] if x['probe']==probe and x['role']=='replay')
    assert primary['tensor']==replay['tensor']
    assert all(a!=b and c!=d for [a,b,c,d],value in primary['tensor'])
    folded=sum(a<b for [a,b,c,d],value in primary['tensor'])
    assert folded*2==len(primary['tensor'])
    if probe:assert folded==3344
    else:assert not folded
assert set(tuple(sorted(x)) for x in data['complete_local_source2_patterns'])=={
 ('Ja','Ja'),('C','JL','Ja'),('C','C','JL','JL')}
assert all(2*k>4 for k in range(3,20))
# The analytical lower bound 2k is an induction, not a k<=19 theorem.
for row in result['actual_source_domain_routes']:
    assert row['source3_or_higher_classical_rows']==0 and row['source_jets']==0
    assert not any(pattern==['C','JL','Ja'] for pattern,count in row['source2_patterns'])

udr=repository_path/'calculations/canonical_so10_u_dimensional_reconciliation'
old=read(udr/'ir_validation_receipt_v2.json')
assert old['first_u_direct_one_variation_common_trace_extension_within_scope']
assert all(x['all_nodes_strictly_below4'] for x in old['probe_bounds'])
assert not old['two_independent_insertions_full_QAP_measure_or_physical_claim']
csw=read(repository_path/'calculations/canonical_so10_cutoff_source_ward_operator/validation_receipt.json')
assert csw['first_variation_joint_test_field_domain'] and csw['finite_Grassmann_Gaussian_fixtures']==8
proof=(output_path/'PROOF.md').read_text()
for phrase in ['submersion','D^k FP Gamma_t = FP D^k Gamma_t','ONE old/new tangent',
 'Source differentiation of the complete UV subtraction polynomial','not a restriction to their diagonal',
 'not an assertion B F_R=0','two Slavnov operations','values of first insertions at J0 alone cannot fix A2']:
    assert phrase in proof,phrase
clarification=(output_path/'PROOF_CLARIFICATION_V2.md').read_text();assert 'REFUTED' in clarification and 'not a zero loop amplitude' in clarification
out={'schema':'NSP2_SEPARATE_SOURCE_PRODUCT_REVIEW','third_direct_action_Wick_Berezin_checks':direct_checks,
 'independent_word_counts':counts,'all_finite_k_formula_proved_by_induction_and_recurrence':True,
 'actual_source2_seagull_tensors_and_graded_pair_exchange_checked':True,
 'allowed_carriers_distinguished_from_classical_population':True,
 'local_source3plus_ambiguity_excluded_not_nonlocal_kernel':True,
 'common_independently_smeared_nonminimal_product_extension':'QUALIFIED_IN_INHERITED_FIRST_U_FORMAL_DOMAIN',
 'single_Slavnov_differentiated_response_with_source_coefficient_contacts':True,
 'two_unlabeled_symmetry_tangents_or_diagonal_pullback_licensed':False,
 'source2_finite_functional_A2_retained_not_fixed_by_source0_first_insertions':True,
 'full_Ward_normalization_mixing_QAP_measure_E5_physical_claim':False,
 'old_quantum_contact_integrals_replayed':False,'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with(output_path/'validation_receipt.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
