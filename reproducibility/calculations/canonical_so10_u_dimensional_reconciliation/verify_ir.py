from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time,sympy as s
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'calculations/canonical_so10_u_F_fourth_support'))
import operators as OP
O=Path(__file__).resolve().parent
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest()
for pp,h in read(O/'ir_review_preparation.json')['input_sha256'].items():assert H(Path(pp))==h,pp
a=read(O/'ir_support_result_v2.json');pp=O/'ir_support_tables_v2.json.gz';assert H(pp)==a['packed_tables_sha256'];data=json.loads(gzip.decompress(pp.read_bytes()))
old=(O/'ir_support.py').read_text();new=(O/'ir_support_v2.py').read_text()
old=old.replace("for label,L,R in [('left',newedge,pole),('right',pole,newedge)]:\n        for k,v in merged(L,R,M0+M0adj).items()","for label,left_bounds,right_bounds in [('left',newedge,pole),('right',pole,newedge)]:\n        for k,v in merged(left_bounds,right_bounds,M0+M0adj).items()")
old=old.replace("O/'ir_preparation.json'","O/'ir_preparation_v2.json'").replace("O/'ir_support_tables.json.gz'","O/'ir_support_tables_v2.json.gz'").replace("O/'ir_support_result.json'","O/'ir_support_result_v2.json'")
assert old==new
failed=read(O/'ir_capture.json');assert failed['execution_state']=='FAILED' and not failed['calculation_completed'] and "unsupported operand type(s) for /: 'dict' and 'str'" in failed['stdout_and_stderr']

# Independent max-plus closure for arbitrarily many OLD constant vertices.
nodes=['B','L','x','C','a'];free={('B','B'):2,('B','L'):1,('L','B'):1,('x','x'):0,('C','a'):2,('a','C'):2}
constants=[('x','x',0),('L','x',0),('x','L',0)];neg=-10000
T={(i,j):max([free[i,k]-d for k,l,d in constants if l==j and (i,k) in free],default=neg) for i in nodes for j in nodes}
K={(i,j):max(T[i,j],0 if i==j else neg) for i in nodes for j in nodes}
for k in nodes:
    for i in nodes:
        for j in nodes:K[i,j]=max(K[i,j],K[i,k]+K[k,j])
assert all(K[i,i]==0 for i in nodes)
dressed={}
for i in nodes:
    for j in nodes:
        v=max((K[i,k]+free[k,j] for k in nodes if (k,j) in free),default=neg)
        if v>neg//2:dressed[i,j]=v
assert dressed=={('B','B'):2,('B','L'):1,('L','B'):1,('B','x'):1,('x','B'):1,('x','x'):0,('C','a'):2,('a','C'):2}
def compose(left,right,blocks):
    out={}
    for a0 in nodes:
        for b0 in nodes:
            vals=[left[a0,i]+right[j,b0]-degree for i,j,degree in blocks if (a0,i) in left and (j,b0) in right]
            if vals:out[a0,b0]=max(vals)
    return out
M0=[('B','C',1),('a','L',0),('C','B',1),('L','a',0)]
checked=[]
for row,tables in zip(a['results'],data['tables']):
    assert row['probe']==tables['probe']
    for i,j,ext,nd,p,c in tables['Hu_full_four_momentum']:
        assert not ext and nd in [0,1] and nd+OP.JP.dimension(i)+OP.JP.dimension(j)+sum(p)==4
    for out,inp,p,nd in tables['Mu_support']:assert nd+OP.JP.dimension(inp)+sum(p)==OP.JP.dimension(out)+1
    H=[tuple(v) for v in row['actual_constant_Hu_blocks']];M=[tuple(v) for v in row['actual_constant_Mu_blocks']];M+=[(j,i,d) for i,j,d in M]
    G1=compose(dressed,dressed,H);assert [[*k,v] for k,v in sorted(G1.items())]==row['inserted_edge_bounds']
    vals=list(compose(dressed,dressed,M).values())+list(compose(G1,dressed,M0).values())+list(compose(dressed,G1,M0).values())
    ordinary=max(G1.values(),default=0);one=max(vals,default=0)
    assert ordinary==row['new_edge_maximum_pole']<=2 and one==row['one_tangent_maximum_merged_pole']<=3
    assert all(z['affine_Euler_nonzero']==0 for z in row['input_route_audits'])
    assert row['positive_mass_scalar_reference_required'] and row['actual_paired_FJB_support_matched']>0
    checked.append({'probe':row['probe'],'ordinary_inserted_degree':ordinary,'first_variation_merged_degree':one,'all_nodes_strictly_below4':True})
assert a['results'][1]['actual_scalar_tangent_present'] and a['results'][1]['massless_scalar_control_merged_degree']==4
bad=compose(dressed,dressed,[('a','C',0)]);assert max(bad.values())==4
r=s.symbols('r',positive=True);integrals={str(v):str(s.integrate(r**(3-v),(r,0,1))) for v in [2,3]}
assert integrals=={'2':'1/2','3':'1'} and s.integrate(1/r,(r,0,1))==s.oo
P=R/'calculations/canonical_so10_joint_born_ir_trace_domain';prior=read(P/'validation_receipt.json')
assert prior['qualified_analytic_proof_version']=='DERIVATION_V2.md' and H(P/'DERIVATION_V2.md')==prior['input_sha256'][str(P/'DERIVATION_V2.md')]
proof=(P/'DERIVATION_V2.md').read_text();assert 'BOTH sides of EVERY free reference' in proof and 'UV finite part first,then' in proof
out={'schema':'UDR4_FIRST_U_IR_BOUND_AND_DOMAIN_REVIEW','actual_first_u_constant_hypotheses_match_inherited_domain':True,'arbitrary_old_constant_chain_closure_proved_by_nonpositive_cycles':True,
 'engineering_degrees_and_all_operator_entries_checked':True,'probe_bounds':checked,'radial_local_L1_controls':integrals,
 'massless_scalar_and_ghost_mass_critical_controls_detected':True,'accepted_old_analytic_domain':'DERIVATION_V2.md;positive_scalar_reference_masses;Schwartz;A0;UV_FP_then_IR',
 'first_u_direct_one_variation_common_trace_extension_within_scope':True,'two_independent_insertions_full_QAP_measure_or_physical_claim':False,
 'V1_failure_preserved_not_PASS_and_exact_alias_fix_checked':True,'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with (O/'ir_validation_receipt.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
