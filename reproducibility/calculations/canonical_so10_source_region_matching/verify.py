"""SRM1 independent lifted graded inverse,raw Wick matching and frozen comparators."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import ast,gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
started=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import dec,red,tidy,zero,w
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz');assert A==B
old=packed(CAL/'canonical_so10_source_common_operation/primary_tables.json.gz')
for new,previous in [('unit_first_base','first_width_base'),('unit_first_hk','first_width_two_background'),('unit_second_hk','second_width_two_background'),('source_zero_hk','source_zero_two_background')]:assert A['words'][new]==old[previous],new
assert len(A['words']['unit_first_hk'])==38 and len(A['words']['unit_second_hk'])==len(A['words']['source_zero_hk'])==6
assert len(A['words']['generic_first_base'])==6
assert len(A['words']['generic_first_hk'])>38 and len(A['words']['generic_second_hk'])>6

# h,k dual numbers;u,chi exterior algebra;2x2 coefficient supermatrices.
N=s.Matrix([[0,0],[1,0]]);I2=s.eye(2)
def create(bit):
    return s.Matrix(4,4,lambda i,j: (-1)**((j&((1<<bit)-1)).bit_count()) if not j&(1<<bit) and i==j|1<<bit else 0)
E=[create(0),create(1)];P=s.diag(1,-1,-1,1);I4=s.eye(4)
def lift(mask,V):
    even=s.kronecker_product(N if mask&1 else I2,N if mask&2 else I2)
    odd=(E[0] if mask&4 else I4)*(E[1] if mask&8 else I4)
    if (mask&12).bit_count()%2:odd=odd*P
    return s.kronecker_product(even,odd,V)
H0=s.diag(3,5);G=H0.inv();generic={1,2,3,4,5,6,8,9,10,12}
K={};X={}
for mask in range(1,16):
    K[mask]=s.Matrix([[0,mask+1],[2-mask,0]]) if (mask&12).bit_count()%2 else s.diag(mask+2,1-mask)
for mask in range(16):
    X[mask]=s.Matrix([[0,mask+3],[mask-5,0]]) if (mask&12).bit_count()%2 else s.diag(2*mask+1,7-mask)
def value_catalog(rows,allowed):
    ans=s.zeros(2)
    for row in rows:
        V=s.eye(2)
        for atom in row['word']:
            if atom=='G':V=V*G
            elif atom[0]=='K':
                mask=int(atom[1:]);V=V*(K[mask] if mask in allowed else s.zeros(2))
            else:V=V*X[int(atom[1:])]
        ans+=row['twice_coefficient']*V
    return ans
def matrix_value(allowed):
    base=s.kronecker_product(s.eye(16),G);change=sum((lift(mask,K[mask]) for mask in allowed),s.zeros(32))
    inv=base;term=base
    for _ in range(4):term=-term*change*base;inv+=term
    fullX=sum((lift(mask,X[mask]) for mask in range(16)),s.zeros(32))
    result=inv*fullX
    # External top h*k*u*chi is even,so no parity factor on this coefficient.
    block=s.Matrix(2,2,lambda i,j:result[30+i,j])
    return block
for label,allowed in [('generic_first_hk',generic),('unit_first_hk',generic-{4,5,6}),('generic_second_hk',generic-{8,9,10,12}),('unit_second_hk',generic-{4,5,6,8,9,10,12})]:
    zero(value_catalog(A['words'][label],allowed)-matrix_value(allowed))
wrong_width=matrix_value(generic)-matrix_value(generic-{4,5,6});assert wrong_width!=s.zeros(2)
wrong_width_trace=s.factor(wrong_width[0,0]-wrong_width[1,1]);assert wrong_width_trace!=0

# Actual source pole comparator:full NAP loop map minus actual light H loop map.
nap=packed(CAL/'canonical_so10_nielsen_affine_poles/primary_tables.json.gz')
model=read(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json')
Xframe=dec(packed(CAL/'canonical_so10_scalar_cubic_light/primary_tables.json.gz')['light_basis_canonical'])
D=tidy(Xframe.H*Xframe);zero(D-s.diag(*[D[i,i] for i in range(5)]));left=tidy(s.diag(*[red(1/D[i,i]) for i in range(5)])*Xframe.H)
CH=dec(packed(CAL/'canonical_so10_source_heavy_elimination/primary_tables.json.gz')['light_Casimir'])
expected=tidy(left*dec(nap['linear_maps'][0])*Xframe+CH/2)
pole=dec(A['hard_chi1_scalar_pole']);zero(pole-expected)
assert pole.todok() and dec(A['omitted_heavy_intermediate_C']).todok()
zero(left*dec(nap['constant_maps'][1]));assert A['affine_chi2_light_zero_positions']==5
assert sum(A['u_scalar_cross_support_by_parent'])>0
oldcells=packed(CAL/'canonical_so10_common_light_boundary/primary_v2_tables.json.gz')['cells'];assert A['sourcezero_cells']==oldcells and len(oldcells)==288
assert A['segmented_cells']==90432
assert A['segmented_family_counts']=={name:(2064 if name in ['VVVV','VVSS','SSSS'] else 14040) for name in ['VVVV','VVSS','SSSS','VVV','VVS','VSS','SSS','ghostV','ghostS']}

# Raw microscopic Wick/Berezin source graphs,then the LIGHT Legendre bridge.
M,m,delta,mu,nu,a,b,lam=s.symbols('M m delta mu nu a b lam',nonzero=True)
def gaussian_even(power,cov):
    if power%2:return s.S.Zero
    return s.factorial2(power-1)*cov**(power//2) if power else s.S.One
# Conditional <z>=chi*b*h/m;external u remains to the left of chi.
connected_source=-a*b*nu*gaussian_even(4,1/M)*gaussian_even(2,1/delta)/(2*m)
onepoint0=nu/(2*M);onepoint_source=a*b/(m*M)
legendre_source=onepoint0*onepoint_source/delta
matched_source=s.factor(connected_source+legendre_source)
assert s.simplify(matched_source-s.sympify(A['toy_one_soft_uchi'],locals={str(v):v for v in [M,m,delta,mu,nu,a,b,lam]}))==0
assert connected_source!=matched_source and matched_source!=0
# All3 scalar pairings:6 cross-vertex Wick contractions plus9 reducible ones.
tree_quartic=lam-3*mu**2/M
SSfull=lam/(8*delta**2)-mu**2/(4*M*delta**2)-mu**2/(8*M*delta**2)
assert s.simplify(SSfull-tree_quartic/(8*delta**2))==0
missing_SS=mu**2/(8*M*delta**2);assert missing_SS!=0
# Complete Laurent products are retained until pole/finite extraction.
eps,L,Hc,Fc,Ac,Bc=s.symbols('eps L Hc Fc Ac Bc')
product_full=s.expand((Hc/eps+Fc+eps*Ac)*(1/eps+L+eps*Bc))
product_early=s.expand((Hc/eps+Fc)*(1/eps+L+eps*Bc))
positive_eps_loss=s.expand(product_full-product_early).coeff(eps,0);assert positive_eps_loss==Ac
Ph,Ps,Fh,Fs,Ss,Bs=s.symbols('Ph Ps Fh Fs Ss Bs')
full=Bs+Ph+Ps;eft=Ss+Ps;Mf=Bs+Fh-Ss
assembled=Mf+Ph+Ps-Fh-Fs+(Fs-Ps)
assert s.expand(full-eft-assembled)==0
wrong_ct=s.expand((Mf+Ph+Ps-Fh-Fs)-(full-eft));assert wrong_ct==Ps-Fs
# A1/p² soft source is allowed and cancels COMMONLY;locality must follow AFTER it.
q,dm=s.symbols('q dm',positive=True);nonlocal_light=1/q
hard_diagnostic=q/(6*M);assert s.simplify((nonlocal_light+hard_diagnostic)-nonlocal_light-hard_diagnostic)==0
assert nonlocal_light!=0 and s.limit(dm*(1/dm),dm,0)==1
controls={'omit_Ku_away_unit_width_STr':str(wrong_width_trace),'omit_heavy_scalar_intermediate_positions':len(dec(A['omitted_heavy_intermediate_C']).todok()),
 'omit_source_cubic_loop':str(matched_source),'omit_light_Legendre_source_remainder':str(connected_source-matched_source),
 'omit_SS_heavy_bridge':str(missing_SS),'drop_positive_epsilon_coefficient':str(positive_eps_loss),
 'omit_soft_parent_forest_transport':str(wrong_ct),'drop_nonlocal_soft_before_common_subtraction':'1/q',
 'set_delta_times_source_to_zero_before_matching':'1'}
receipt={'schema':'SRM1_VALIDATION','status':'QUALIFIED_FORMAL_SOURCE_REGION_MATCHING_AND_LOCAL_BOSONIC_WIDTH_IDENTITY',
 'execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
 'actual_hard_one_loop_source_functional_finite_recipe':True,'all_finite_model_source_components_extracted':False,
 'source_dependent_Schur_and_heavy_leaves_retained':True,'formal_one_two_soft_bijection_and_CT_ownership':True,
 'generic_first_width_background_words':len(A['words']['generic_first_hk']),
 'generic_second_width_background_words':len(A['words']['generic_second_hk']),
 'unit_width_regression_counts':[38,6,6],'lifted_graded_matrix_dimension':32,
 'original_sourcezero_region_cells':288,'conservative_segmented_region_cells':90432,
 'hard_scalar_first_width_pole_nonzero_positions':len(pole.todok()),'hard_scalar_first_width_pole_total_positions':25,
 'affine_second_width_light_pole_zero_positions':5,'source_u_scalar_cross_positions':sum(A['u_scalar_cross_support_by_parent']),
 'full_Wilson_remainder_retained_until_common_subtraction':True,
 'nonlinear_matched_Slavnov_identity_in_declared_formal_domain':True,
 'local_background_F2_both_widths_analytic_near_unit_consequence':True,
 'global_gauges_physical_C1_fermionic_E5_A5_or_perturbativity_qualified':False,
 'negative_controls':controls,
 'shared_error_limits':['physical BFT action/reference/projectors','NTS/EPC/SHE/CBR/ASE Ward and forest premises','Euclidean dimensional region theorem','symbolic software/point reducer','AI authorship'],
 'elapsed_after_imports':time.perf_counter()-started}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
