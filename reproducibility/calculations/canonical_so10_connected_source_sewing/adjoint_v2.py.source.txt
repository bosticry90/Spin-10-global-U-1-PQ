from pathlib import Path
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as J
from coefficient_ring import expression,coefficient,g,xi,eta
read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'adjoint_preparation_v2.json')['input_sha256'].items():assert digest(Path(p))==h,p
def extract(flows):
    action={}
    for mu in range(4):
        entries={}
        for r in range(45):
            for w,c in flows.get(4*r+mu,{}).items():
                if len(w)!=2 or any(js for f,js in w):continue
                bs=[f//4 for f,js in w if f<180 and f%4==mu]
                cs=[f-553 for f,js in w if 553<=f<565]
                if len(bs)==len(cs)==1:entries[cs[0],r,bs[0]]=c
        action[mu]=entries
    assert all(z==action[0] for z in action.values())
    return action[0]
def strip(c):
    assert all(a==1 and b==d==0 for (a,b,d,root),v in c.terms)
    return expression(tuple(((0,b,d,root),v) for (a,b,d,root),v in c.terms))
def matrix_rows(entries):
    d={}
    for (h,r,t),c in entries.items():d.setdefault((h,t),{})[r]=strip(c)
    return s.SparseMatrix(len(d),45,{(i,r):v for i,z in enumerate(d.values()) for r,v in z.items()})
um=load(R/'calculations/canonical_so10_u_maximal_heat_cutoff/primary_inputs.json.gz')
fj=load(R/'calculations/canonical_so10_full_jet_source_master_bridge/replay_tables.json.gz')
fields={i:J.decode(z) for i,z in um['field_flows']}
replay={i:J.decode(z) for i,z in fj['operation']}
A=extract(fields);AA=extract(replay);assert A==AA
assert all((r<12)==(t<12) for h,r,t in A)
beta={}
for r in range(45):
    for w,c in fields.get(508+r,{}).items():
        if len(w)!=2 or any(js for f,js in w):continue
        ls=[f-508 for f,js in w if 508<=f<553];cs=[f-553 for f,js in w if 553<=f<565]
        if len(ls)==len(cs)==1:beta[cs[0],r,ls[0]]=c
beta_replay={}
for w,c in um['source_action']:
    if len(w)==3 and 0<=w[0]<45 and 135<=w[1]<147 and 225<=w[2]<270:
        beta_replay[w[1]-135,w[0],w[2]-225]=coefficient(s.sympify(c,locals={'g10':g,'xi':xi,'eta_H':eta}))
assert beta_replay==beta
project={key:c for key,c in A.items() if key[1]>=12 and key[2]>=12}
keys=set(beta)|set(project)
diff={key:beta.get(key,J.ZERO)-project.get(key,J.ZERO) for key in keys}
diff={key:c for key,c in diff.items() if c}
assert not diff,('RESTRICTED_BRST_VS_ADJOINT_MISMATCH',len(diff))
MA=matrix_rows(A);MB=matrix_rows(beta);basis=MA.nullspace()
assert all(MA*b==s.zeros(MA.rows,1) and MB*b==s.zeros(MB.rows,1) for b in basis)
old=load(O/'sewing_tables.json.gz')
conditional=[]
for probe in [0,1]:
    cols=next(z['canonical_K_even_plane'] for z in old['routes'] if z['role']=='primary' and z['probe']==probe and 'canonical_K_even_plane' in z)
    K={i:J.decode(z) for i,z in cols}
    grad={i-508:J.decode(z) for i,z in um['GF_gradient'] if 508<=i<553}
    F={i:{w:c for w,c in z.items() if len(w)==2 and all(f<180 and not js for f,js in w)} for i,z in grad.items()}
    for b,vector in enumerate(basis):
        projected={}
        for r,z in K.items():
            weight=coefficient(vector[r])
            for w,c in z.items():
                if len(w)==2 and all(f<180 and not js for f,js in w):J.put(projected,w,-J.times(weight,c))
                if len(w)==1 and w[0][0]<180 and w[0][1]==(0,) and w[0][0]%4==0:
                    # Each divergence has the same coefficient in four directions;
                    # select mu=0 once, never sum it four times.
                    col=w[0][0]//4
                    for ww,v in F.get(col,{}).items():J.put(projected,ww,J.times(J.times(weight,c),J.times(-J.I,v)))
        conditional.append({'probe':probe,'basis':b,'remainder':J.encode(J.clean(projected))})
result={'schema':'CNS1B_ADJOINT_RECONCILIATION','actual_qB_H_adjoint_entries':len(A),
 'actual_qLambda_H_entries':len(beta),'four_Lorentz_routes_equal':True,'FJB_replay_equal':True,
 'H_M_blocks_preserved':True,'qLambda_equals_M_projected_qB':True,
 'adjoint_invariant_covectors':[[str(v) for v in b] for b in basis],
 'adjoint_invariant_dimension':len(basis),'restricted_BRST_invariant_dimension':45-MB.rank(),
 'adjoint_invariants_in_restricted_BRST_annihilator':True,'projected_BB_tests':conditional,
 'actual_renormalized_tadpole_membership':'NOT_ESTABLISHED','full_connected_extension':'NOT_ESTABLISHED',
 'elapsed_after_imports':time.perf_counter()-tick,'scientific_acceptance':'NOT_PERFORMED'}
with(O/'adjoint_result_v2.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps({k:v for k,v in result.items() if k!='adjoint_invariant_covectors'},sort_keys=True),flush=True);timer.cancel()
