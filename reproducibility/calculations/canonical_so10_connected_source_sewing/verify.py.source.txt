from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import gzip,json,os,sys,threading,time
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as J
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'review_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
data=json.loads(gzip.decompress((O/'sewing_tables.json.gz').read_bytes()));native=read(O/'native_result.json')
assert digest(O/'sewing_tables.json.gz')==native['packed_tables_sha256']
assert native['full_connected_distributional_extension']=='NOT_ESTABLISHED'
assert read(O/'native_capture.json')['execution_state']=='COMPLETED'

bosons=[];odds=[]
for row in data['fixtures']['bosonic']:
    seed=row['seed'];k,g,r1,r2,t1,t2,p,c=map(F,[seed+2,seed+1,seed+2,seed+3,seed+5,seed+7,seed+2,seed+3])
    v1,v2,w1,w2=map(F,[1,2,3,4])
    # Differentiate the closed stationary one-loop answer with respect to u.
    expected=(w1*t2+t1*w2)/(2*k*k)-p*t1*t2/k**3-g*(w1*r2+t1*v2+w2*r1+t2*v1)/k**3+3*g*p*(t1*r2+t2*r1)/k**4+g*g*(v1*r2+r1*v2)/k**4-4*p*g*g*r1*r2/k**5+g*c/(2*k*k)
    assert F(row['W1_uab'])==expected==sum(map(F,row['five_terms_u']))
    assert all(F(v) for v in row['five_terms_u']) and all(row['all_omissions_sensitive'])
    assert F(row['source_pair_mean_contact'])==g*c/(2*k*k)
    bosons.append(str(expected))
for row in data['fixtures']['odd']:
    seed=row['seed'];k,m,g,Y,p,q,c,r,t=map(s.Rational,[seed+2,seed+3,seed+1,seed+4,seed+2,seed+1,seed+3,1,2])
    u,h=s.symbols('u h');K=k+u*p;M=m+u*q
    # Integrate f0,f1 FIRST. Gaussian/cubic scalar moments through one loop.
    mz=-g*h/(2*K**2);mz2=h/K
    ratio=(1+u*(r+t))/(h*(M+Y*mz))-u*c/h*(M*mz+Y*mz2)/(M+Y*mz)
    w=s.series(h*ratio,h,0,2).removeO().coeff(h,1)
    expected=s.diff(w,u).subs(u,0)
    assert s.cancel(expected-s.Rational(row['W1_uab_theta12']))==0
    assert row['odd_exchange_sensitive'] and row['Schur_and_direct_Wick_agree']
    assert F(row['source_pair_mean_contact'])!=0
    odds.append(str(expected))

for probe in [-1,0,1]:
    aa=[x for x in data['routes'] if x['probe']==probe and 'first_columns' in x]
    assert len(aa)==2 and {k:v for k,v in aa[0].items() if k!='role'}=={k:v for k,v in aa[1].items() if k!='role'}
    cols={i:J.decode(z) for i,z in aa[0]['first_columns']}
    ids=set(range(1151,1196))|set(range(1241,1286))
    assert set(cols)|set(aa[0]['zero_first_column_ids'])==ids and not(set(cols)&set(aa[0]['zero_first_column_ids']))
    assert not aa[0]['affine_second_source_columns']
    for i,rows in aa[0]['affine_endpoints']:
        assert i>=1241
        for w,c in J.decode(rows).items():
            assert len(w)==1 and w[0][0]<553
            f,js=w[0]
            assert (f<180 and len(js)==1) or (f>=180 and not js)
    assert len(aa[0]['source_only_pair_contacts'])=={ -1:0,0:12,1:33}[probe]

# Independently reconstruct the restricted BRST coefficient nullspace from
# the source action, not the stored field flow. It is NOT a background theorem.
um=json.loads(gzip.decompress((R/'calculations/canonical_so10_u_maximal_heat_cutoff/primary_inputs.json.gz').read_bytes()))
rows={};g10=s.symbols('g10')
for word,value in um['source_action']:
    if len(word)==3 and 0<=word[0]<45 and 135<=word[1]<147 and 225<=word[2]<270:
        key=(word[1]-135,word[2]-225)
        rows.setdefault(key,{})[word[0]]=s.cancel(s.sympify(value)/g10)
matrix=s.SparseMatrix(len(rows),45,{(i,j):v for i,d in enumerate(rows.values()) for j,v in d.items()})
basis=[s.Matrix([s.sympify(x) for x in b]) for b in data['H_invariant_auxiliary_covectors']]
assert len(basis)==13 and s.Matrix.hstack(*basis).rank()==13
assert matrix.rank()==32 and all(matrix*b==s.zeros(matrix.rows,1) for b in basis)
assert all(not row['K_D_F_D_inverse_F_BB_minus_K_BB'] for row in data['projected_auxiliary_BB_test'])
assert 'NOT accepted as covariance theorems' in (O/'COVARIANCE_CLARIFICATION.md').read_text()

# Independent exact Gaussian limit and finite-part transport diagnostics.
r=s.symbols('r',positive=True);profile=1-2/(1+r*r)**2+1/(1+2*r*r)**2
limits=[s.limit(profile,r,0),profile.subs(r,1),s.limit(profile,r,s.oo)]
assert limits==[0,s.Rational(11,18),1]
t,a,b,T0,T1=s.symbols('t a b T0 T1')
sewn=(T0+t*T1)*(a/t+b)
fp=s.expand(sewn).coeff(t,0);proper=s.limit((T0+t*T1)*b,t,0)
assert s.expand(fp-proper)==T1*a
assert read(O/'preparation.json')['input_sha256'][str(R/'project_state.json')]==digest(R/'project_state.json')
result={'schema':'CNS1A_INDEPENDENT_REVIEW','execution_state':'COMPLETED',
 'supported':'actual left-Euler source endpoints; nonlinear finite connected identity; necessary affine soft bound',
 'bosonic_values':bosons,'odd_values':odds,'delta_smoothing_path_limits':[str(x) for x in limits],
 'proper_before_sewing_finite_difference':str(fp-proper),
 'restricted_BRST_nullspace_dimension':13,'native_background_covariance_interpretation':'NOT_ACCEPTED_SEE_CLARIFICATION',
 'full_connected_extension':'NOT_ESTABLISHED','state_unchanged':True,
 'elapsed_after_imports':time.perf_counter()-tick,'scientific_acceptance':'NOT_PERFORMED'}
with(O/'validation_receipt.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(result,sort_keys=True),flush=True);timer.cancel()
