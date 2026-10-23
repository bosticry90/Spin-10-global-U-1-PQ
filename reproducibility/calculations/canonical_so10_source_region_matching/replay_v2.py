"""SRM1 inverse recursion,representation Gram and exact conditional heavy integral."""
from data_v2 import *
from itertools import combinations,product
from collections import Counter
started=begin('replay')
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import dec,enc,red,tidy,zero
def sign(a,b):
    if a&b:return 0
    p=lambda m:((m&12).bit_count()%2)
    return (-1)**(p(a)*p(b)+bool(a&8 and b&4))
def inverse(allowed):
    out={0:{('G',):1}}
    for mask in sorted(range(1,16),key=int.bit_count):
        rows={}
        for j in allowed:
            if j&mask!=j:continue
            rest=mask^j;sgn=sign(j,rest)
            for word,c in out[rest].items():
                key=('G','K'+str(j))+word;rows[key]=rows.get(key,0)-sgn*c
        out[mask]={w:c for w,c in rows.items() if c}
    return out
def op(allowed,target):
    inv=inverse(allowed);rows={}
    for mask,terms in inv.items():
        if mask&target!=mask:continue
        other=target^mask;sgn=sign(mask,other)
        for word,c in terms.items():
            key=word+('X'+str(other),);rows[key]=rows.get(key,0)+sgn*c
    return [{'twice_coefficient':int(c),'word':list(w)} for w,c in sorted(rows.items()) if c]
generic={1,2,3,4,5,6,8,9,10,12};unit=generic-{4,5,6};second=generic-{8,9,10,12}
words={'generic_first_base':op(generic,12),'generic_first_hk':op(generic,15),
 'unit_first_base':op(unit,12),'unit_first_hk':op(unit,15),
 'generic_second_hk':op(second,15),'unit_second_hk':op(second-{4,5,6},15),'source_zero_hk':op(generic,3)}

d=read(PACKET/'full_replay.json')
X=dec(packed(CAL/'canonical_so10_scalar_cubic_light/replay_tables.json.gz')['light_basis_canonical'])
H=tidy(X.H*X);zero(H-s.diag(*[H[i,i] for i in range(5)]));invH=s.diag(*[red(1/H[i,i]) for i in range(5)])
left=tidy(invH*X.H);zero(left*X-s.eye(5))
fullgram=s.zeros(5);crossgram=s.zeros(5);u_counts=[]
for a in range(45):
    R=s.SparseMatrix(s.diag(*[dec(d['representation_matrices'][k][a]) for k in ['Phi','Sigma','phi','S']]))
    RX=tidy(R*X);U=tidy(left*RX);Y=tidy(RX-X*U)
    fullgram=tidy(fullgram+RX.H*RX);crossgram=tidy(crossgram+Y.H*Y);u_counts.append(len(Y.todok()))
she=packed(CAL/'canonical_so10_source_heavy_elimination/replay_tables.json.gz')
CM=tidy(invH*fullgram-dec(she['light_Casimir']));omitted=tidy(invH*crossgram);assert omitted.todok()
nap=packed(CAL/'canonical_so10_nielsen_affine_poles/replay_tables.json.gz');zero(left*dec(nap['constant_maps'][1]))
print('STAGE replay_full_virtual_scalar_intermediates_retained',flush=True)

census=packed(CAL/'canonical_so10_soft_region_support_closure/replay_tables.json.gz')['census'];cells=[]
for row in census:
    bits=row['light_bits'];n=len(bits);regions=[[],[0],[1],list(range(n))]+([[2]] if n==3 else [])
    for soft in regions:
        if row['kind']=='STRUCTURAL_ZERO':fate='STRUCTURAL_VERTEX_ZERO'
        elif not soft:fate='PURE_LIGHT_COMMON_HH' if all(bits) else 'RETAIN_HARD_INPUT'
        elif len(soft)==1:
            if bits[soft[0]]==0:fate='SCALELESS_TAYLOR_CONTACT_AFTER_EXPANSION'
            elif all(bits):fate='PURE_LIGHT_COMMON_HS'
            else:fate={1:'ORDINARY_HARD_OPENING',2:'INTERNAL_LIGHT_HARD_OPENING_TSR'}[sum(bits)]
        elif all(bits):fate='COMMON_LIGHT_TREE_SS'
        elif sum(bits)==2 and n==3:fate={'SSS':'INDUCED_SCALAR_QUARTIC_SS','VSS':'HIGHER_DIMENSION_TREE_SS'}[row['family']]
        else:fate='SCALELESS_TAYLOR_CONTACT_AFTER_EXPANSION'
        cells.append({'family':row['family'],'mass_bits':bits,'soft_momentum_edges':soft,'fate':fate})
cells.sort(key=lambda v:(v['family'],v['mass_bits'],v['soft_momentum_edges']))
families={'VVVV':2,'VVSS':2,'SSSS':2,'VVV':3,'VVS':3,'VSS':3,'SSS':3,'ghostV':3,'ghostS':3};segmented=[]
for family,n in families.items():
    regions=[(),(0,),(1,),tuple(range(n))]+([(2,)] if n==3 else [])
    for length in range(n,n+5):
        for cuts in combinations(range(1,length),n-1):
            ends=(0,)+cuts+(length,);pieces=tuple(ends[j+1]-ends[j] for j in range(n))
            for mask in range(1<<length):
                bits=tuple((mask>>j)&1 for j in range(length))
                for soft in regions:segmented.append((family,pieces,bits,soft))
segmented.sort();digest=sha256()
for row in segmented:digest.update((json.dumps(row,separators=(',',':'))+'\n').encode())

def creation(bit):
    return s.SparseMatrix(16,16,{(mask|1<<bit,mask):(-1)**((mask&((1<<bit)-1)).bit_count()) for mask in range(16) if not mask&(1<<bit)})
u,chi,z,bar=[creation(i) for i in range(4)]
M,m,delta,mu,nu,a,b,lam=s.symbols('M m delta mu nu a b lam',nonzero=True);h,x,theta=s.symbols('h x theta')
ghost=m*bar*z+a*h*x*u*z+b*h*chi*bar
exp=s.eye(16)-ghost+ghost*ghost/2
kappa=s.factor(-exp[15,0]/exp[12,0]/(h*h*x));assert s.simplify(kappa-a*b/m)==0
ne=nu+2*theta*kappa;mass=M+ne*x
E0=delta*x*x/2+lam*x**4/24-mu**2*x**4/(8*mass)
Fh=s.log(mass)/2-s.log(m)
le=s.factor(s.diff(E0,x,4).subs({x:0,theta:0}))
source=s.factor(s.diff(s.diff(Fh,x,2),theta).subs({x:0,theta:0})/(2*delta))
assert s.simplify(source+nu*kappa/(M*M*delta))==0
finish('replay',{'words':words,'coset_C_soft':enc(CM),'hard_chi1_scalar_pole':enc(tidy(-CM/2)),
 'omitted_heavy_intermediate_C':enc(omitted),'u_scalar_cross_support_by_parent':u_counts,
 'affine_chi2_light_zero_positions':5,'sourcezero_cells':cells,
 'segmented_cells':len(segmented),'segmented_catalog_sha256':digest.hexdigest(),
 'segmented_family_counts':dict(Counter(row[0] for row in segmented)),
 'toy_lambda_eff':str(le),'toy_one_soft_uchi':str(source),
 'toy_SS_sunset':str(-mu**2/(4*M*delta**2)),'toy_SS_bridge':str(-mu**2/(8*M*delta**2)),
 'hard_word_bound_weight4':4,'higher_Wilson_weights_defined_by_finite_recipe':True,
 'actual_source_region_construction':True,'all_finite_source_components_extracted':False,
 'physical_numerical_C1_or_E5_A5_qualified':False},started)
