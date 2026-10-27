from pathlib import Path
from hashlib import sha256
from collections import Counter
from functools import lru_cache
from fractions import Fraction
import ast,gzip,json,os,sys,threading,time
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'calculations/canonical_so10_full_jet_source_master_bridge'))
import jets as J
from coefficient_ring import coefficient,expression,g,xi,eta
from nonlinear import bosonic,odd
read=lambda p:json.loads(p.read_bytes())
load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
source_ids=set(range(1151,1196))|set(range(1241,1286))
def kind(i):
    return 'B' if i<180 else 'x' if i<508 else 'L' if i<553 else 'C' if i<598 else 'a' if i<643 else 'JL' if 1151<=i<1196 else 'Ja' if i>=1241 else 'otherJ'
@lru_cache(None)
def co(v):return coefficient(s.sympify(v,locals={'g10':g,'xi':xi,'eta_H':eta}))
def convert(i):return 1151+i if i<45 else 1241+i-45 if i<90 else 1196+i-90 if i<135 else 553+i-135 if i<180 else 598+i-180 if i<225 else 508+i-225
def raw_euler(poly,ids):
    out={}
    for word,value in poly.items():
        for at,(i,js) in enumerate(word):
            if i not in ids:continue
            sign=(-1)**(J.parity(i)*sum(J.parity(f) for f,ds in word[:at])+len(js))
            remaining={word[:at]+word[at+1:]:value*sign}
            J.add(out.setdefault(i,{}),J.Ds(remaining,js))
    return {i:J.clean(z) for i,z in out.items() if J.clean(z)}
def enc_columns(cols):return [[i,J.encode(z)] for i,z in sorted(cols.items())]
def restrict(poly,allowed):return {w:c for w,c in poly.items() if all(i in allowed for i,js in w)}
def affine(cols):return {i:{w:c for w,c in z.items() if len(w)==1 and w[0][0]<643} for i,z in cols.items()}
def fields_only(z):return {w:c for w,c in z.items() if all(i<643 for i,js in w)}
tables=[];metadata=[];last=None
for role in ['primary','replay']:
    um=load(R/'calculations/canonical_so10_u_maximal_heat_cutoff'/(role+'_inputs.json.gz'))
    fj=load(R/'calculations/canonical_so10_full_jet_source_master_bridge'/(role+'_tables.json.gz'))
    deriv=J.euler if role=='primary' else raw_euler
    base={}
    for w,c in um['source_action']:J.put(base,tuple((convert(i),()) for i in w),co(c))
    base=J.clean(base)
    for probe in [-1,0,1]:
        poly=base if probe==-1 else J.decode(um['QG'][probe])
        cols=deriv(poly,source_ids)
        first={i:fields_only(z) for i,z in cols.items()};first={i:J.clean(z) for i,z in first.items() if J.clean(z)}
        endpoint=affine(first)
        # Ordered second source columns before source restriction.
        pairs=[];pair_affine=[];pair_contact=[]
        for i,z in sorted(cols.items()):
            for j,zz in sorted(deriv(z,source_ids).items()):
                keep=fields_only(zz)
                if keep:pairs.append([i,j,J.encode(keep)])
                aa={w:c for w,c in keep.items() if len(w)==1}
                cc=keep.get((),J.ZERO)
                if aa:pair_affine.append([i,j,J.encode(aa)])
                if cc:pair_contact.append([i,j,J.encode({():cc})])
        assert not pair_affine,('ACTUAL_S_PHI_JJ_AT_ZERO_NONZERO',role,probe)
        row={'role':role,'probe':probe,'density_rows':len(poly),
          'first_columns':enc_columns(first),'affine_endpoints':enc_columns(endpoint),
          'second_source_columns':pairs,'source_only_pair_contacts':pair_contact,
          'affine_second_source_columns':pair_affine,'zero_first_column_ids':sorted(source_ids-set(first))}
        tables.append(row)
        shapes=Counter((kind(i),kind(w[0][0]),len(w[0][1])) for i,z in endpoint.items() for w in z)
        metadata.append({'role':role,'probe':probe,'density_rows':len(poly),
          'first_nonzero_columns':len(first),'first_rows':sum(map(len,first.values())),
          'affine_rows':sum(map(len,endpoint.values())),
          'affine_shapes':[[list(k),v] for k,v in sorted(shapes.items())],
          'ordered_second_columns':len(pairs),'source_only_pair_contacts':len(pair_contact),
          'S_phi_JJ_at_zero_rows':0})
    # Canonical shear on even-source plane, used only to expose the tadpole test.
    plane=set(range(553))|set(range(1241,1286))
    for probe,packet in enumerate(fj['probes']):
        generator=J.decode(packet['G']);gc=deriv(generator,source_ids)
        K={i-1151:restrict(z,plane) for i,z in gc.items() if i<1196}
        tables.append({'role':role,'probe':probe,'canonical_K_even_plane':enc_columns(K)})
    if role=='primary':last=(um,fj)
    print('STAGE '+role+' actual endpoints '+str(time.perf_counter()-tick),flush=True)
for probe in [-1,0,1]:
    p=next(x for x in tables if x.get('role')=='primary' and x.get('probe')==probe and 'first_columns' in x)
    q=next(x for x in tables if x.get('role')=='replay' and x.get('probe')==probe and 'first_columns' in x)
    assert {k:v for k,v in p.items() if k!='role'}=={k:v for k,v in q.items() if k!='role'}
for probe in [0,1]:
    p=next(x for x in tables if x.get('role')=='primary' and x.get('probe')==probe and 'canonical_K_even_plane' in x)
    q=next(x for x in tables if x.get('role')=='replay' and x.get('probe')==probe and 'canonical_K_even_plane' in x)
    assert p['canonical_K_even_plane']==q['canonical_K_even_plane']

um,fj=last;flow={i:J.decode(z) for i,z in um['field_flows']}
constraints={}
for r in range(45):
    for word,c in flow.get(508+r,{}).items():
        if len(word)!=2:continue
        ghosts=[i-553 for i,js in word if 553<=i<598 and not js]
        aux=[i-508 for i,js in word if 508<=i<553 and not js]
        if len(ghosts)==len(aux)==1 and ghosts[0]<12:
            # Common factor g10 is symbolic, removed only from the linear
            # covariance constraint, not inverted in a counterterm ring.
            expr=s.cancel(expression(c.terms)/g)
            assert not expr.has(g,xi,eta)
            constraints.setdefault((ghosts[0],aux[0]),{})[r]=expr
matrix=s.SparseMatrix(len(constraints),45,{(row,col):v for row,d in enumerate(constraints.values()) for col,v in d.items()})
basis=matrix.nullspace();assert all(matrix*b==s.zeros(matrix.rows,1) for b in basis)
invariants=[[str(v) for v in b] for b in basis]
gf={i:J.decode(z) for i,z in um['GF_gradient'] if 508<=i<553}
fbb={i-508:{w:c for w,c in z.items() if len(w)==2 and all(j<180 and not js for j,js in w)} for i,z in gf.items()}
fd={}
for i,z in gf.items():
    ds={w:c for w,c in z.items() if len(w)==1 and w[0][0]<180 and len(w[0][1])==1}
    assert ds=={((4*(i-508)+mu,(mu,)),):J.I for mu in range(4)},('GAUGE_DIVERGENCE_NOT_I_ID',i)
    fd[i-508]=ds
projected=[]
for probe in [0,1]:
    columns=next(x['canonical_K_even_plane'] for x in tables if x.get('role')=='primary' and x.get('probe')==probe and 'canonical_K_even_plane' in x)
    K={i:J.decode(z) for i,z in columns}
    kb={i:{w:c for w,c in z.items() if len(w)==2 and all(j<180 and not js for j,js in w)} for i,z in K.items()}
    kd={}
    for r,z in K.items():
        dd={w:c for w,c in z.items() if len(w)==1 and w[0][0]<180 and len(w[0][1])==1}
        grouped={}
        for w,c in dd.items():
            f,js=w[0];assert js==(f%4,),('NON_DIVERGENCE_K_LEG',r,w)
            grouped.setdefault(f//4,{})[f%4]=c
        for v in grouped.values():assert len(v)==4 and all(c==v[0] for c in v.values())
        kd[r]={color:v[0] for color,v in grouped.items()}
    for b,vector in enumerate(basis):
        defect={};project_k={}
        for r,z in kb.items():J.add(project_k,z,co(str(vector[r])))
        for r,ds in kd.items():
            for col,c in ds.items():
                for w,v in fbb.get(col,{}).items():J.put(defect,w,J.times(J.times(co(str(vector[r])),c),J.times(-J.I,v)))
        J.add(defect,project_k,-1);defect=J.clean(defect)
        projected.append({'probe':probe,'H_invariant_basis':b,'K_BB_rows':len(J.clean(project_k)),
          'K_D_F_D_inverse_F_BB_minus_K_BB':J.encode(defect)})

fixtures={'bosonic':[bosonic(seed) for seed in range(1,5)],'odd':[odd(seed) for seed in range(1,5)]}
out={'schema':'CNS1A_SOURCE_ENDPOINT_AND_NONLINEAR_SEWING_DATA','routes':tables,
 'H_invariant_auxiliary_covectors':invariants,'covariance_constraint_rank':45-len(basis),
 'projected_auxiliary_BB_test':projected,'fixtures':fixtures}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())+len(blob)<16*1024**2
with(O/'sewing_tables.json.gz').open('xb') as f:f.write(blob)
result={'schema':'CNS1A_NATIVE_RESULT','actual_endpoint_metadata':metadata,
 'H_invariant_dimension':len(basis),'H_covariant_projected_BB_remainders':[len(x['K_D_F_D_inverse_F_BB_minus_K_BB']) for x in projected],
 'nonlinear_bosonic_fixture_values':[x['W1_uab'] for x in fixtures['bosonic']],
 'nonlinear_odd_fixture_values':[x['W1_uab_theta12'] for x in fixtures['odd']],
 'packed_tables_sha256':sha256(blob).hexdigest(),'elapsed_after_imports':time.perf_counter()-tick,
 'full_connected_distributional_extension':'NOT_ESTABLISHED','scientific_acceptance':'NOT_PERFORMED'}
with(O/'native_result.json').open('xb') as f:f.write((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(result,sort_keys=True),flush=True);timer.cancel()
