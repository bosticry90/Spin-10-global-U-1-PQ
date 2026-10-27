from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import gzip,json,os,sys,threading,time
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as J
from coefficient_ring import coefficient,expression,g
read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'late_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
result=read(O/'adjoint_result_v2.json');assert read(O/'adjoint_capture_v2.json')['execution_state']=='COMPLETED'
assert read(O/'adjoint_capture.json')['execution_state']=='FAILED'
assert "unhashable type: 'list'" in read(O/'adjoint_capture.json')['stdout_and_stderr']
assert not(O/'adjoint_result.json').exists()
fj=load(R/'calculations/canonical_so10_full_jet_source_master_bridge/primary_tables.json.gz')
ops={i:J.decode(z) for i,z in fj['operation']}
matrix=s.zeros(12*45,45)
for r in range(45):
    for word,c in ops[4*r+3].items():
        if len(word)!=2 or any(js for f,js in word):continue
        vec=[f//4 for f,js in word if f<180 and f%4==3]
        gh=[f-553 for f,js in word if 553<=f<565]
        if len(vec)==len(gh)==1:matrix[45*gh[0]+vec[0],r]+=s.cancel(expression(c.terms)/g)
basis=[s.Matrix(list(map(s.sympify,b))) for b in result['adjoint_invariant_covectors']]
assert len(basis)==2 and matrix.rank()==43 and s.Matrix.hstack(*basis).rank()==2
assert all(matrix*b==s.zeros(matrix.rows,1) for b in basis)
um=load(R/'calculations/canonical_so10_u_maximal_heat_cutoff/replay_inputs.json.gz')
gf={i-508:J.decode(z) for i,z in um['GF_gradient'] if 508<=i<553}
F={i:{w:c for w,c in z.items() if len(w)==2 and all(f<180 and not js for f,js in w)} for i,z in gf.items()}
tables=load(O/'sewing_tables.json.gz');checks=[]
for probe in [0,1]:
    generator=J.decode(fj['probes'][probe]['G'])
    # Fresh source Euler differentiation from the other full-jet route.
    raw=J.euler(generator,set(range(1151,1196)))
    plane=set(range(553))|set(range(1241,1286))
    K={i-1151:{w:c for w,c in z.items() if all(f in plane for f,js in w)} for i,z in raw.items()}
    for b,vector in enumerate(basis):
        left={};right={}
        for r,z in K.items():
            weight=coefficient(vector[r])
            for w,c in z.items():
                if len(w)==2 and all(f<180 and not js for f,js in w):J.put(right,w,J.times(weight,c))
                if len(w)==1 and w[0][0]<180 and w[0][0]%4==3 and w[0][1]==(3,):
                    for ww,v in F.get(w[0][0]//4,{}).items():J.put(left,ww,J.times(J.times(weight,c),J.times(-J.I,v)))
        left=J.clean(left);right=J.clean(right)
        assert left==right,('ADJOINT_TADPOLE_POLYNOMIAL_REPLAY_MISMATCH',probe,b)
        checks.append({'probe':probe,'basis':b,'left_rows':len(left),'right_rows':len(right),'difference_rows':0})
assert all(not x['remainder'] for x in result['projected_BB_tests'])
assert result['qLambda_equals_M_projected_qB'] and result['H_M_blocks_preserved']
assert result['actual_renormalized_tadpole_membership']=='NOT_ESTABLISHED'
assert result['full_connected_extension']=='NOT_ESTABLISHED'
assert digest(R/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
out={'schema':'CNS1B_ADJOINT_LATE_REVIEW','execution_state':'COMPLETED','exact_adjoint_rank':43,
 'invariant_dimension':2,'source_Euler_and_spatial_divergence_replay':checks,
 'actual_tadpole_membership_and_complete_mean_response':'NOT_ESTABLISHED',
 'full_connected_QAP_or_physical_claim':False,'state_unchanged':True,
 'elapsed_after_imports':time.perf_counter()-tick,'scientific_acceptance':'NOT_PERFORMED'}
with(O/'late_validation_receipt.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
