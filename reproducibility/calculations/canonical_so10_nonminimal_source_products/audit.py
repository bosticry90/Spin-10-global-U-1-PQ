from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import combinations_with_replacement,permutations
import gzip,json,os,sys,threading,time
repository_path=Path(__file__).resolve().parents[2];output_path=Path(__file__).resolve().parent
sys.path.insert(0,str(repository_path/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as JP
from finite_algebra import fixture
read=lambda p:json.loads(p.read_bytes());loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
for path,digest in read(output_path/'preparation.json')['input_sha256'].items():assert file_hash(Path(path))==digest,path
def load(folder,name):return loadz(repository_path/'calculations'/folder/name)
def gh(i):
    return (-1-gh(i-643)) if i>=643 else 1 if 553<=i<598 else -1 if 598<=i<643 else 0
def kind(i):return 'Ja' if i>=1241 else 'JL' if 1151<=i<1196 else 'C' if 553<=i<598 else 'other'
def raw_remove(word,token):
    result=[]
    for at,t in enumerate(word):
        if t==token:
            sign=(-1)**(JP.parity(token[0])*sum(JP.parity(x[0]) for x in word[:at]))
            result.append((word[:at]+word[at+1:],sign))
    return result
routes=[];seagulls=[]
for role in ['primary','replay']:
    data=load('canonical_so10_u_maximal_heat_cutoff',role+'_inputs.json.gz')
    source_action=JP.decode(data['source_action'])
    assert max(sum(i>=643 for i,jets in w) for w in source_action)<=1
    for probe in range(2):
        poly=JP.decode(data['QG'][probe]);retained={w:c for w,c in poly.items() if JP.degree(w,4) in [0,1]}
        patterns=Counter();source2={};source_jets=0
        for word,value in retained.items():
            assert sum(gh(i) for i,jets in word)==0
            assert sum(JP.parity(i) for i,jets in word)%2==0
            sources=[i for i,jets in word if i>=643]
            assert len(sources)<=2 and all(kind(i) in ['Ja','JL'] for i in sources)
            source_jets+=sum(len(jets) for i,jets in word if i>=643)
            if len(sources)==2:
                assert JP.degree(word,4)==0 and all(not jets for i,jets in word)
                pattern=tuple(sorted(kind(i) for i,jets in word));patterns[pattern]+=1;source2[word]=value
        assert set(patterns)<={('Ja','Ja'),('C','JL','Ja'),('C','C','JL','JL')}
        assert source_jets==0
        paired={w:c for w,c in source2.items() if all(kind(i) in ['JL','C'] for i,jets in w)}
        tensor={}
        if role=='primary':
            pair_ids=sorted({i for w in paired for i,jets in w if kind(i)=='JL'})
            for a in pair_ids:
                first=JP.leftjet(paired,(a,()))
                second_ids={i for w in first for i,jets in w if kind(i)=='JL'}
                for b in second_ids:
                    second=JP.leftjet(first,(b,()))
                    for w,v in second.items():
                        assert len(w)==2 and all(kind(i)=='C' for i,jets in w)
                        for c,d in permutations([i for i,jets in w]):
                            final=JP.leftjet(JP.leftjet({w:v},(c,())),(d,()))
                            value=final.get((),JP.ZERO)
                            key=(a,b,c,d);tensor[key]=tensor.get(key,JP.ZERO)+value
        else:
            for word,value in paired.items():
                js=[i for i,jets in word if kind(i)=='JL'];cs=[i for i,jets in word if kind(i)=='C']
                for a,b in permutations(js):
                    for c,d in permutations(cs):
                        terms=[(word,1)]
                        for token in [a,b,c,d]:terms=[(ww,sign*sg) for w,sign in terms for ww,sg in raw_remove(w,(token,()))]
                        assert all(not ww for ww,sign in terms)
                        key=(a,b,c,d);tensor[key]=tensor.get(key,JP.ZERO)+sum(sign for ww,sign in terms)*value
        tensor={k:v for k,v in tensor.items() if v}
        for (a,b,c,d),value in tensor.items():
            assert tensor.get((b,a,c,d),JP.ZERO)==-value
            assert tensor.get((a,b,d,c),JP.ZERO)==-value
        routes.append({'role':role,'probe':probe,'retained_density_rows':len(retained),
          'source2_patterns':[[list(k),v] for k,v in sorted(patterns.items())],
          'source2_rows':len(source2),'source_jets':source_jets,
          'actual_H_JJ_ghost_pair_entries':len(tensor),'source3_or_higher_classical_rows':0})
        seagulls.append({'role':role,'probe':probe,'tensor':[[list(k),[[list(p),v.numerator,v.denominator] for p,v in value.terms]] for k,value in sorted(tensor.items())]})
assert seagulls[0]['tensor']==seagulls[2]['tensor'] and seagulls[1]['tensor']==seagulls[3]['tensor']
assert not seagulls[0]['tensor'] and seagulls[1]['tensor']
# Independent carrier enumeration, not source-field word counts.
ordinary=[('B',1,0),('x',1,0),('L',2,0),('C',1,1),('a',1,-1),('d',1,0),('nu',1,0)]
allowed=[]
for ja in range(3):
    jl=2-ja;source_dim=2*ja+jl;source_gh=-jl
    for n in range(5):
        for rest in combinations_with_replacement(ordinary,n):
            if source_dim+sum(x[1] for x in rest)==4 and source_gh+sum(x[2] for x in rest)==0:
                allowed.append(['Ja']*ja+['JL']*jl+[x[0] for x in rest])
assert sorted(sorted(x) for x in allowed)==sorted([['Ja','Ja'],['C','JL','Ja'],['C','C','JL','JL']])
fixtures=[fixture(seed) for seed in range(1,5)]
tables={'schema':'NSP1_ACTUAL_SOURCE_POLYNOMIAL_AND_GAUSSIAN_DATA','routes':routes,
 'actual_H_JJ_tensors':seagulls,'complete_local_source2_patterns':allowed,'finite_Grassmann_gaussian_checks':fixtures,
 'operator_program':{'base_H_source_degree':1,'U_source_degree':2,'u_derivatives':1,
  'source_k_formula':'1/2 sum_{S subset labels, |S|<=2} (-1)^(k-|S|) sum_perm(complement) STr[G A...G U_S]',
  'two_source_terms':['G Uij','-G Uj G Ai','-G Aj G Ui','G U0 G Aj G Ai','G Aj G U0 G Ai'],
  'Slavnov_response':'D_labels(B F_R)=sum_S (D_S B) R_complement; retain coefficient derivatives',
  'local_source3plus_ambiguity':'excluded by 2k>4; nonlocal product is not zero'}}
raw=(json.dumps(tables,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
assert sum(p.stat().st_size for p in output_path.iterdir() if p.is_file())+len(blob)<16*1024**2
with(output_path/'product_tables.json.gz').open('xb') as f:f.write(blob)
result={'schema':'NSP1_NONMINIMAL_SOURCE_PRODUCT_CONSTRUCTION','actual_source_domain_routes':routes,
 'all_actual_H_JJ_components_agree':True,'quadratic_source_seagull_nonzero_for_broken_probe':True,
 'four_genuine_Grassmann_Gaussian_Berezinian_checks':True,
 'all_five_ordered_terms_required_in_fixtures':True,'local_source3plus_counterterms_excluded':True,
 'old_quantum_contact_tensors_newly_integrated':False,
 'common_extension_analytic_claim_requires_separate_review':True,
 'no_full_QAP_measure_E5_or_physical_claim':True,'scientific_acceptance':'NOT_PERFORMED',
 'packed_tables_sha256':sha256(blob).hexdigest(),'elapsed_after_imports':time.perf_counter()-tick}
with(output_path/'product_result.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(result,sort_keys=True),flush=True);timer.cancel()
