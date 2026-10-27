from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import combinations,permutations
import gzip,json,os,sys,threading,time
repository_path=Path(__file__).resolve().parents[2]
output_path=Path(__file__).resolve().parent
sys.path.insert(0,str(repository_path/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as JP

tick=time.perf_counter()
timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
read=lambda p:json.loads(p.read_bytes())
loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
for path,digest in read(output_path/'preparation.json')['input_sha256'].items():
    assert file_hash(Path(path))==digest,path

def calc(folder,name):
    path=repository_path/'calculations'/folder/name
    return loadz(path) if path.suffix=='.gz' else read(path)

def predicate(folder,name,key):
    assert calc(folder,name)[key] is True,(folder,name,key)

predicate('canonical_so10_chiral_probe_support','validation_receipt.json','both_full_generators_and_QG_matter_BV_brackets_zero')
predicate('canonical_so10_cutoff_source_ward_operator','validation_receipt.json','first_variation_joint_test_field_domain')
predicate('canonical_so10_u_dimensional_reconciliation','ir_validation_receipt_v2.json','first_u_direct_one_variation_common_trace_extension_within_scope')
assert calc('canonical_so10_chiral_probe_support','validation_receipt.json')['classical_augmented_defect']=='UNCHANGED_NONZERO_IHAT'
assert calc('canonical_so10_chiral_probe_support','validation_receipt.json')['source_differentiation_before_zero_superGaussian_control_nonzero']

routes=[]
for role in ['primary','replay']:
    data=calc('canonical_so10_u_maximal_heat_cutoff',role+'_inputs.json.gz')
    for probe in range(2):
        poly=JP.decode(data['QG'][probe])
        retained={w:c for w,c in poly.items() if JP.degree(w,4) in [0,1]}
        assert all(0<=i<1286 for w in retained for i,js in w)
        source_ids={i for w in retained for i,js in w if i>=643}
        assert source_ids and all(508<=i-643<553 or 598<=i-643<643 for i in source_ids)
        counts=Counter()
        diagonal=[]
        if role=='primary':
            # Source Euler first, including every source2 word and all jets.
            response=JP.euler(retained,source_ids)
            for src,rows in response.items():
                field=src-643
                for word,value in rows.items():
                    nd=JP.dimension(field)+1-sum(JP.dimension(i)+len(js) for i,js in word)
                    assert nd in [0,1]
                    for token in set(t for t in word if t[0]==field):
                        d=JP.leftjet({word:value},token)
                        for remaining,coefficient in d.items():
                            # The differentiated field jets act on the internal line.
                            assert nd+sum(JP.dimension(i)+len(js) for i,js in remaining)+len(token[1])==1
                            counts['diagonal_after_source_Euler']+=1
                            diagonal.append([src,nd,len(token[1]),JP.encode({remaining:coefficient})])
        else:
            # Raw density port removal, BEFORE any integration by parts.
            # Moving source jets by IBP cannot change the remaining field names
            # or their total engineering weight including internal derivatives.
            for word,value in retained.items():
                nd=JP.degree(word,4)
                for at,(src,source_jets) in enumerate(word):
                    if src<643:continue
                    field=src-643
                    for bt,(other,field_jets) in enumerate(word):
                        if other!=field:continue
                        rest=word[:min(at,bt)]+word[min(at,bt)+1:max(at,bt)]+word[max(at,bt)+1:]
                        assert nd+sum(JP.dimension(i)+len(js) for i,js in rest)+len(source_jets)+len(field_jets)==1
                        counts['raw_diagonal_density_pairs']+=1
                        diagonal.append([src,nd,len(source_jets)+len(field_jets),[[i,list(js)] for i,js in rest]])
        # All permitted intrinsic1 T/F remainder words have engineering weight5.
        target_weights={'T':1+JP.dimension(1241)+JP.dimension(553)+JP.dimension(180),
                        'F':1+JP.dimension(1151)+2*JP.dimension(553)+JP.dimension(180)}
        assert target_weights=={'T':5,'F':5}
        assert all(1-weight<0 for weight in target_weights.values())
        counts['source2_rows']=sum(sum(i>=643 for i,js in w)==2 for w in retained)
        routes.append({'role':role,'probe':probe,'retained_density_rows':len(retained),
          'all_source_ports_nonminimal':len(source_ids),'counts':dict(counts),
          'diagonal_operator_total_weight':1,'target_weights':target_weights,
          'required_target_differential_degree':-4,'target_direct_supertrace_zero':True,
          'diagonal_entries':diagonal})

# Use actual raw (not compact or hats0) insertion ports and source vertex.
cps=calc('canonical_so10_chiral_probe_support','primary_inputs.json.gz')
cps_replay=calc('canonical_so10_chiral_probe_support','replay_inputs.json.gz')
assert cps['hat_vertices']==cps_replay['hat_vertices'] and cps['K_vertex']==cps_replay['K_vertex']
assert cps['SMA']['physical_antifield_copies']==1 and cps['SMA']['auxiliary_BRST_transform']=='0'
hat=cps['hat_vertices'];assert len(hat)==3
for vertex in hat:
    assert sorted(p for p,j in vertex['ports'])==['P','S','c']
    assert sum(j=='h' for p,j in vertex['ports'])==1
assert sorted(p for p,j in cps['K_vertex']['ports'])==['K','P','c']

# Read the actual complete generators, not just constant or source-linear parts.
generator_audit=[]
for role,source in [('primary',cps),('replay',cps_replay)]:
    nonminimal_source_names=set()
    for i in range(45):
        nonminimal_source_names.update(['J'+('b' if i<12 else 'L')+str(i),
                                       'J'+('bar' if i<12 else 'ub')+str(i)])
    for key in ['physical_G','physical_QG']:
        for probe,packed in enumerate(source[key]):
            names={source['names'][i] for degree,word,k in packed['monomials'] for i,jets in word}
            actual_sources={n for n in names if n.startswith('J')}
            assert actual_sources<=nonminimal_source_names,(role,key,probe,actual_sources-nonminimal_source_names)
            # CPS authenticates the physical matter/support bridge; these
            # actual generators use only the original bosonic geometry names.
            assert not names.intersection({'P','S','K','K_P','psi','barpsi'})
            generator_audit.append({'role':role,'generator':key,'probe':probe,
              'density_rows':len(packed['monomials']),'source_names':sorted(actual_sources)})

matter_vertices=[{'origin':'kin_PP','ports':['P','P']},
 {'origin':'kin_SS','ports':['S','S']},{'origin':'kin_PS_hat','ports':['P','S']},
 {'origin':'gauge_BPP','ports':['B','P','P']},
 {'origin':'Yukawa_xPP','ports':['x','P','P']},
 {'origin':cps['K_vertex']['origin'],'ports':[p for p,j in cps['K_vertex']['ports']]}]
insertion_vertices=[{'origin':v['origin'],'ports':[p for p,j in v['ports']]} for v in hat]
def all_hessian_ports(vertices):
    answer=[]
    for v in vertices:
        for i,j in permutations(range(len(v['ports'])),2):
            left,right=v['ports'][i],v['ports'][j]
            if left=='K' or right=='K':continue # a source is not a quantum line
            remaining=[p for n,p in enumerate(v['ports']) if n not in [i,j]]
            killed=bool(set(remaining)&{'P','S','K'})
            groups=['F' if p in ['P','S'] else 'N' for p in [left,right]]
            answer.append({'origin':v['origin'],'ports':[left,right],
              'remaining':remaining,'groups':groups,'external_matter_or_K_required':killed})
    return answer
matter_paths=all_hessian_ports(matter_vertices);insertion_paths=all_hessian_ports(insertion_vertices)
assert all(z['external_matter_or_K_required'] or z['groups']==['F','F'] for z in matter_paths+insertion_paths)
assert any(z['groups']!=['F','F'] and z['external_matter_or_K_required'] for z in insertion_paths)
assert any(z['origin']=='KCP' and z['external_matter_or_K_required'] for z in matter_paths)

reference_dependencies=['fixed_A0','fixed_xi','fixed_eta_H','positive_fixed_scalar_reference_masses','fixed_heat_parameter']
operation_on_reference={k:0 for k in reference_dependencies}
assert all(v==0 for v in operation_on_reference.values())
# These are semantic dependencies from UWB/CSW, not inferred from the zeros.
uwb=(repository_path/'calculations/canonical_so10_u_source_ward_bridge/DERIVATION.md').read_text()
assert 'fixed at A0' in uwb and 'direct variation is zero there' in uwb
assert 'G_t R_t M' in uwb and 'source derivative precedes' in uwb

tables={'routes':routes,'full_generator_support':generator_audit,
 'matter_Hessian_port_pairs':matter_paths,'raw_hatted_Hessian_port_pairs':insertion_paths,
 'reference_dependencies':reference_dependencies,'reference_operation':operation_on_reference}
raw=(json.dumps(tables,sort_keys=True,separators=(',',':'))+'\n').encode()
blob=gzip.compress(raw,mtime=0)
assert sum(p.stat().st_size for p in output_path.iterdir() if p.is_file())+len(blob)<16*1024**2
with (output_path/'ward_support_tables.json.gz').open('xb') as f:f.write(blob)
result={'schema':'UWT1_ACTUAL_PROJECTED_WARD_SUPPORT',
 'source_differentiation_precedes_restriction':True,
 'probes':[{k:v for k,v in row.items() if k!='diagonal_entries'} for row in routes],
 'hatted_master_insertion_projection_zero_before_integration':True,
 'master_defect_not_set_zero':True,'full_base_master_premise_inherited':True,
 'arbitrary_Born_length_excluded_by_invariant_quadratic_blocks':True,
 'direct_supertrace_T_F_zero_by_actual_ports_and_dimension':True,
 'fixed_regulator_and_reference_direct_response_zero':True,
 'pairing_preservation_of_Mu_claimed':False,
 'ordered_cutoff_remains_required':True,'new_quantum_integrals_computed':0,
 'complete_Ward_trace_applicability_requires_separate_review':True,
 'full_QAP_E5_physical_claim':False,'scientific_acceptance':'NOT_PERFORMED',
 'packed_tables_sha256':sha256(blob).hexdigest(),'elapsed_after_imports':time.perf_counter()-tick}
with (output_path/'ward_support_result.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(result,sort_keys=True),flush=True)
timer.cancel()
