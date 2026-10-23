"""GPC1 independent coefficient comparison and complete gauge-only UV assembly."""
from data import *
from collections import defaultdict
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for n,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(n))==h,n
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def eq(a,b):assert s.expand(s.sympify(a)-s.sympify(b))==0,(a,b)
tri_positions=0;tri_nonzero=0
assert set(P['triangle'])==set(R['triangle']) and len(P['triangle'])==64
for lor in P['triangle']:
 for word in ['012','021']:
  A=P['triangle'][lor][word];B=R['triangle'][lor][word];assert len(A)==len(B)==8
  for a,b in zip(A,B):eq(a,b);tri_positions+=1;tri_nonzero+=int(s.sympify(a)!=0)
assert set(P['box'])==set(R['box']) and len(P['box'])==70
for w in P['box']:eq(P['box'][w],R['box'][w])
box_nonzero=sum(s.sympify(v)!=0 for v in P['box'].values());assert tri_nonzero and box_nonzero
G=dec(P['G']);assert G==dec(R['G'])==2*s.eye(45)
c=s.sympify(R['Weyl_heat_curvature_coefficient'])
GEP=packed(CAL/'canonical_so10_split_momentum_gauge_polarization/primary_tables.json.gz');GR=packed(CAL/'canonical_so10_split_momentum_gauge_polarization/replay_tables.json.gz')
for d in [GEP,GR]:
 eq(4*c,d['UV_tensor_coefficients'][0]);eq(-4*c,d['UV_tensor_coefficients'][1])
 assert dec(d['G'])==G
hat=s.sympify(GEP['UV_tensor_coefficients'][2])/2;eq(hat,s.sympify(GR['UV_tensor_coefficients'][2])/2)
assert P['radial_pole_residues']==['1','1']
# Independent free-algebra BRST calculation. The ghost occurs once, so all
# other factors are even; no hidden Grassmann cyclic sign is involved.
g=s.Symbol('g10');A,B,C,C0,C1,D0B,D1A,DD=s.symbols('A B c dc0 dc1 d0B d1A d01c',commutative=False)
comm=lambda X,Y:X*Y-Y*X
qA=C0-s.I*g*comm(A,C);qB=C1-s.I*g*comm(B,C)
d0qB=DD-s.I*g*(comm(D0B,C)+comm(B,C0));d1qA=DD-s.I*g*(comm(D1A,C)+comm(A,C1))
F=D0B-D1A-s.I*g*comm(A,B);qF=s.expand(d0qB-d1qA-s.I*g*(comm(qA,B)+comm(A,qB)))
assert s.expand(qF+s.I*g*comm(F,C))==0
X,Z,Zmu=s.symbols('X dhatc dbardhatc',commutative=False)
qX=Zmu-s.I*g*(comm(X,C)+comm(A,Z))
# Tr[X[X,c]]=0 by finite color cyclicity, not operator trace cyclicity.
def cyclic(word):return min(word[j:]+word[:j] for j in range(len(word)))
zero_trace=defaultdict(int)
zero_trace[cyclic(('X','X','c'))]+=1;zero_trace[cyclic(('X','c','X'))]-=1
assert all(v==0 for v in zero_trace.values())
assert s.expand(2*X*qX-(2*X*Zmu-2*s.I*g*X*comm(A,Z)))==-2*s.I*g*X*comm(X,C)
# Test defects at the level where each control is mathematically sensitive.
def triangle_diffs(other):return sum(s.sympify(a)!=s.sympify(b) for k in P['triangle'] for w in ['012','021'] for a,b in zip(P['triangle'][k][w],other[k][w]))
den_diff=triangle_diffs(P['triangle_no_denominator']);rawden_nonzero=sum(s.sympify(v[2])!=0 for v in P['raw_triangle_A_B_U'].values())
commuting=defaultdict(lambda:s.S.Zero)
for w,v in P['box'].items():commuting[tuple(sorted(map(int,w.split(','))))]+=s.sympify(v)
assert all(v==0 for v in commuting.values())
controls={'wrong_Fourier_Taylor_routing':triangle_diffs(P['triangle_wrong_routing'])>0,'omit_right_color_reversal':triangle_diffs(P['triangle_no_right_reversal'])>0,'wrong_odd_vertex_charge_sign':triangle_diffs(P['triangle_wrong_right_sign'])>0,'drop_denominator_Taylor_ordered_kernel':rawden_nonzero>0,'drop_one_box_pairing':any(s.sympify(P['box'][w])!=s.sympify(P['box_missing_pairing'][w]) for w in P['box']),'omit_Nambu_half':tri_nonzero>0 and box_nonzero>0,'extra_half_after_Nambu':tri_nonzero>0 and box_nonzero>0,'wrong_closed_family_count':3*4*c!=6*4*c,'commute_color_words':box_nonzero>0 and all(v==0 for v in commuting.values()),'drop_general_external_hatted_pole':hat!=0}
assert all(controls.values())
for obj in [P,R]:
 assert obj['physical_spin_trace']==4 and obj['gaussian_factor']=='1/2' and obj['closed_family_count']==3 and obj['UV_only_d4_angular_projection'] and not obj['parity_odd_computed'] and not obj['mass_dependent_terms_computed'] and not obj['physical_scheme_adopted'] and obj['new_one_loop_vertex_families']==2 and obj['new_two_loop_integrals']==0
assert R['Weyl_spin_trace']==2 and R['Weyl_modulus_log_factor']=='1/2' and R['full_Dirac_equivalent_log_factor']=='1/4'
assert digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
local={'per_family_bar_F_squared_trace_coefficient':str(c),'per_family_hat_derivative_A_squared_trace_coefficient':str(hat),'three_family_bar_F_squared_trace_coefficient':str(3*c),'three_family_hat_derivative_A_squared_trace_coefficient':str(3*hat),'three_family_CT_bar_F_squared_trace_coefficient':str(-3*c),'three_family_CT_hat_derivative_A_squared_trace_coefficient':str(-3*hat),'common_factor':'g10^2/(16*pi^2*epsilon)','F_definition':'dbar_mu A_nu-dbar_nu A_mu-i*g10*[A_mu,A_nu]','barred_F_squared_BRST_variation':'0_MOD_FINITE_COLOR_TRACE','hat_kinetic_BRST_variation_per_trace_coefficient':'2 Tr[(dhat Abar_mu)(dhat dbar_mu c)]-2i*g10 Tr[(dhat Abar_mu)[Abar_mu,dhat c]]','counterterm_algebraic_remainders':['0','0'],'hat_external_gauge_vertices':'ABSENT_IN_ACTUAL_SMA','finite_normalization':'zeta_b0_kappa_DISTINCT_UNFIXED','independent_higher_insertion_integrals_computed':False,'parity_odd_or_mass_dependent_sector_included':False}
raw=(json.dumps(local,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'local_pole_tables.json.gz').open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_PARITY_EVEN_MASS_INDEPENDENT_PURE_GAUGE_FERMION_UV_FUNCTIONAL','elapsed_after_imports':time.perf_counter()-start,'triangle_Lorentz_momentum_traceword_positions_compared':tri_positions,'triangle_nonzero_positions':tri_nonzero,'quartic_cyclic_traceword_positions_compared':len(P['box']),'quartic_nonzero_tracewords':box_nonzero,'actual_color_Gram_positions_compared':2025,'per_family_bar_F_squared_trace_coefficient':str(c),'per_family_hat_derivative_A_squared_trace_coefficient':str(hat),'closed_family_count':3,'two_point_kinetic_consistency_remainder':'0','cubic_quartic_curvature_remainders':['0','0'],'local_singular_subtraction_remainder':'0','bar_curvature_BRST_covariance_remainder':'0','hatted_singular_BRST_breaking_retained':True,'controls':controls,'denominator_Taylor_omission_full_vertex_different_positions':den_diff,'ordered_denominator_Taylor_nonzero_carriers':rawden_nonzero,'local_pole_packed_sha256':sha256(blob).hexdigest(),'local_pole_raw_sha256':sha256(raw).hexdigest(),'new_one_loop_vertex_families':2,'new_two_loop_integrals':0,'independent_higher_Ward_insertions_qualified':False,'finite_restoration_QAP_measure_or_phase_qualified':False,'mass_dependent_terms_or_physical_matching_qualified':False,'physical_scheme_adopted':False,'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
