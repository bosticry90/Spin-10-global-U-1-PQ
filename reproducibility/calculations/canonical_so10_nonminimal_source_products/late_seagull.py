from pathlib import Path
from hashlib import sha256
from functools import lru_cache
from fractions import Fraction
import gzip,json,os,sys,threading,time,sympy as s
repository_path=Path(__file__).resolve().parents[2];output_path=Path(__file__).resolve().parent
sys.path.insert(0,str(repository_path/'calculations/canonical_so10_intrinsic_full_source_descent'))
from coefficient_ring import Coeff,coefficient,g,xi,eta
read=lambda p:json.loads(p.read_bytes());loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for path,digest in read(output_path/'late_preparation.json')['input_sha256'].items():assert file_hash(Path(path))==digest,path
data=loadz(output_path/'product_tables_v3.json.gz');compared=[]
@lru_cache(None)
def parse(text):return coefficient(s.expand(s.sympify(text,locals={'g10':g,'xi':xi,'eta_H':eta,'sqrt':s.sqrt,'I':s.I})))
for role in ['primary','replay']:
    root=repository_path/'calculations/canonical_so10_remaining_u_contact_vertices'
    old=loadz(root/('vertices_'+role+'_tables.json.gz'))
    for probe in range(2):
        native=next(x for x in data['actual_H_JJ_tensors'] if x['role']==role and x['probe']==probe)
        new={tuple(k):Coeff([(tuple(p),Fraction(n,d)) for p,n,d in value]) for k,value in native['tensor'] if k[0]<k[1]}
        earlier={}
        for i,ji,j,jj,ext,value in old['groups']['u'+str(probe)]:
            if not(225<=i<270 and 225<=j<270 and len(ext)==2 and all(315<=a<360 for a in ext)):continue
            assert not ji and not jj and ext[0]<ext[1]
            key=(1151+ext[0]-315,1151+ext[1]-315,553+i-225,553+j-225)
            assert key not in earlier;earlier[key]=parse(value)
        assert earlier==new,('ACTUAL_H_JJ_COORDINATE_OR_HESSIAN_CONVENTION_MISMATCH',role,probe,len(earlier),len(new))
        compared.append({'role':role,'probe':probe,'complete_nonzero_classical_entries':len(new),'all_coefficients_equal':True})
old_code=(output_path/'audit_v2.py').read_text()
new_code=(output_path/'audit_v3.py').read_text()
expected=old_code.replace('from finite_algebra import fixture','from finite_algebra_v2 import fixture').replace("output_path/'preparation_v2.json'","output_path/'preparation_v3.json'").replace("output_path/'product_tables.json.gz'","output_path/'product_tables_v3.json.gz'").replace("output_path/'product_result.json'","output_path/'product_result_v3.json'")
assert expected==new_code
assert read(output_path/'review_capture.json')['execution_state']=='FAILED'
assert read(output_path/'audit_capture_v2.json')['execution_state']=='COMPLETED'
assert read(output_path/'review_capture_v2.json')['execution_state']=='COMPLETED'
assert not(output_path/'validation_receipt.json').exists()
out={'schema':'NSP3_LATE_CLASSICAL_SEAGULL_AND_CONVENTION_REVIEW','comparisons':compared,
 'actual_model_source_derivative_code_unchanged_by_fixture_correction':True,
 'old_classical_Hessian_right_j_left_i_convention_matches':True,
 'new_ordered_source_count_6688_equals_two_source_orders_of_old_3344':True,
 'nativeV2_calculation_completed_but_fixture_interpretation_rejected':True,
 'no_historical_loop_or_quantum_normalization_changed':True,
 'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with(output_path/'late_validation_receipt.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
