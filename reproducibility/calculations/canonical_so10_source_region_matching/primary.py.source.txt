"""SRM1 Leibniz words,actual coset source projection and labelled region cells."""
from data import *
from itertools import product
from collections import Counter
started=begin('primary')
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import dec,enc,red,tidy,zero

def combine(rows):
    out={}
    for coeff,word in rows:
        word=tuple(word);out[word]=out.get(word,0)+coeff
    return {word:c for word,c in out.items() if c}
def derivative(poly,bit):
    rows=[]
    for word,coeff in poly.items():
        for j,atom in enumerate(word):
            if atom=='G':new=[(-1,('G','K'+str(bit),'G'))]
            elif atom.startswith('X'):
                mask=int(atom[1:]);new=[] if mask&bit else [(1,('X'+str(mask|bit),))]
            else:
                mask=int(atom[1:]);allowed={1,2,3,4,5,6,8,9,10,12}
                new=[] if mask&bit or mask|bit not in allowed else [(1,('K'+str(mask|bit),))]
            for sign,piece in new:rows.append((coeff*sign,word[:j]+piece+word[j+1:]))
    return combine(rows)
def encode(poly):return [{'twice_coefficient':int(c),'word':list(word)} for word,c in sorted(poly.items())]
base=combine([(1,('G','X12')),(1,('G','K4','G','X8')),(-1,('G','K8','G','X4')),
 (-1,('G','K12','G','X0')),(-1,('G','K4','G','K8','G','X0')),(1,('G','K8','G','K4','G','X0'))])
full=derivative(derivative(base,1),2)
unit=lambda p:{w:c for w,c in p.items() if not any(a in ['K4','K5','K6'] for a in w)}
second=lambda p:{w:c for w,c in p.items() if not any(a in ['K8','K9','K10','K12'] for a in w)}
zero_words=derivative(derivative({('G','X0'):1},1),2)
words={'generic_first_base':encode(base),'generic_first_hk':encode(full),
 'unit_first_base':encode(unit(base)),'unit_first_hk':encode(unit(full)),
 'generic_second_hk':encode(second(full)),'unit_second_hk':encode(unit(second(full))),
 'source_zero_hk':encode(zero_words)}

model=read(PACKET/'full_primary.json')
X=dec(packed(CAL/'canonical_so10_scalar_cubic_light/primary_tables.json.gz')['light_basis_canonical'])
metric=tidy(X.T*X);aug=s.MutableSparseMatrix(metric.row_join(s.eye(5)))
for j in range(5):
    pivot=next(k for k in range(j,5) if red(aug[k,j])!=0)
    if pivot!=j:aug.row_swap(j,pivot)
    value=red(aug[j,j])
    for k in range(10):aug[j,k]=red(aug[j,k]/value)
    for i in range(5):
        if i==j:continue
        value=red(aug[i,j])
        if value:
            for k in range(10):aug[i,k]=red(aug[i,k]-value*aug[j,k])
left=tidy(aug[:,5:]*X.T);Ps=tidy(X*left)
gc=packed(CAL/'canonical_so10_gauge_coupling_uv/primary_tables.json.gz')
C=s.diag(*[s.sympify(gc['Casimirs'][k]) for k in ['Phi','Sigma','phi','S'] for _ in range(model['sector_dimensions'][k])])
she=packed(CAL/'canonical_so10_source_heavy_elimination/primary_tables.json.gz');CH=dec(she['light_Casimir'])
CM=tidy(left*C*X-CH);pole=tidy(-CM/2);zero(left*C*dec(model['vacuum']['VEV']))
rho=[s.SparseMatrix(s.diag(*[dec(model['representation_matrices'][k][a]) for k in ['Phi','Sigma','phi','S']])) for a in range(45)]
u_counts=[]
for R in rho:
    RX=tidy(R*X);U=tidy(left*RX);Y=tidy(RX-X*U);u_counts.append(len(Y.todok()))
UM=dec(she['broken_soft_scalar_action']);wrong=tidy(-sum((UM[:,5*a:5*a+5]**2 for a in range(45)),s.zeros(5)))
omitted=tidy(CM-wrong);assert omitted.todok()
print('STAGE primary_actual_coset_source_and_u_scalar_vertices',flush=True)

census=packed(CAL/'canonical_so10_soft_region_support_closure/primary_tables.json.gz')['census']
cells=[]
for row in census:
    n=len(row['light_bits']);flows=[(1,0),(0,1)]+([(1,1)] if n==3 else []);regions={}
    for mask in range(1<<n):
        A=s.Matrix([flows[j] for j in range(n) if mask>>j&1]) if mask else s.zeros(0,2)
        rank=A.rank();soft=tuple(j for j,f in enumerate(flows) if A.col_join(s.Matrix([f])).rank()==rank);regions[soft]=rank
    for soft,rank in sorted(regions.items()):
        bits=row['light_bits'];alllight=all(bits)
        if row['kind']=='STRUCTURAL_ZERO':fate='STRUCTURAL_VERTEX_ZERO'
        elif rank==0:fate='PURE_LIGHT_COMMON_HH' if alllight else 'RETAIN_HARD_INPUT'
        elif rank==1:
            if not bits[soft[0]]:fate='SCALELESS_TAYLOR_CONTACT_AFTER_EXPANSION'
            elif alllight:fate='PURE_LIGHT_COMMON_HS'
            else:fate='ORDINARY_HARD_OPENING' if sum(bits)==1 else 'INTERNAL_LIGHT_HARD_OPENING_TSR'
        elif alllight:fate='COMMON_LIGHT_TREE_SS'
        elif n==3 and sum(bits)==2:fate='INDUCED_SCALAR_QUARTIC_SS' if row['family']=='SSS' else 'HIGHER_DIMENSION_TREE_SS'
        else:fate='SCALELESS_TAYLOR_CONTACT_AFTER_EXPANSION'
        cells.append({'family':row['family'],'mass_bits':bits,'soft_momentum_edges':list(soft),'fate':fate})
cells.sort(key=lambda v:(v['family'],v['mass_bits'],v['soft_momentum_edges']))
families={'VVVV':2,'VVSS':2,'SSSS':2,'VVV':3,'VVS':3,'VSS':3,'SSS':3,'ghostV':3,'ghostS':3}
segmented=[]
for family,n in families.items():
    regions=[(),(0,),(1,),tuple(range(n))]+([(2,)] if n==3 else [])
    for lengths in product(range(1,6),repeat=n):
        if sum(lengths)-n>4:continue
        for bits in product([0,1],repeat=sum(lengths)):
            for soft in regions:segmented.append((family,lengths,bits,soft))
segmented.sort();digest=sha256()
for row in segmented:digest.update((json.dumps(row,separators=(',',':'))+'\n').encode())

# Direct Wick factors;the ghost square fixes the external u*chi sign first.
M,m,delta,mu,nu,a,b,lam=s.symbols('M m delta mu nu a b lam',nonzero=True)
kappa=a*b/m
quartic=lam/(8*delta**2);sun_ss=-mu**2/(4*M*delta**2);bridge_ss=-mu**2/(8*M*delta**2)
source_one_soft=-nu*kappa/(M*M*delta)
lambda_eff=s.factor(8*delta**2*(quartic+sun_ss+bridge_ss))
assert s.expand(lambda_eff-(lam-3*mu*mu/M))==0
raw_wick=-s.Rational(3,2)*nu*kappa/(M*M*delta)
light_legendre=s.Rational(1,2)*nu*kappa/(M*M*delta)
polynomial=s.factor(raw_wick+light_legendre)
# Direct contraction above is -3/2,+1/2 times nu*kappa/(M²*delta).
assert s.simplify(polynomial-source_one_soft)==0
finish('primary',{'words':words,'coset_C_soft':enc(CM),'hard_chi1_scalar_pole':enc(pole),
 'omitted_heavy_intermediate_C':enc(omitted),'u_scalar_cross_support_by_parent':u_counts,
 'affine_chi2_light_zero_positions':5,'sourcezero_cells':cells,
 'segmented_cells':len(segmented),'segmented_catalog_sha256':digest.hexdigest(),
 'segmented_family_counts':dict(Counter(row[0] for row in segmented)),
 'toy_lambda_eff':str(lambda_eff),'toy_one_soft_uchi':str(s.factor(source_one_soft)),
 'toy_SS_sunset':str(sun_ss),'toy_SS_bridge':str(bridge_ss),
 'hard_word_bound_weight4':4,'higher_Wilson_weights_defined_by_finite_recipe':True,
 'actual_source_region_construction':True,'all_finite_source_components_extracted':False,
 'physical_numerical_C1_or_E5_A5_qualified':False},started)
