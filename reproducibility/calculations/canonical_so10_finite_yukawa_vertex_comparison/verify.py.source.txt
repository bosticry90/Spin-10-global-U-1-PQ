"""FYV1 full marginal finite proper-vertex comparison, no parameter adoption."""
from data import *
start=time.perf_counter();t=threading.Timer(600,lambda:os._exit(124));t.daemon=True;t.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,hsh in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(p))==hsh,p
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz')
def z(M):assert not s.SparseMatrix(M).applyfunc(s.expand).todok()
expected={'E_F':-4,'E_L':-s.Rational(5,6),'L_F':-s.I/2,'L_L':-5*s.I/6,'R_F':-s.I/2,'R_L':-5*s.I/6}
for key,want in expected.items():
 assert s.simplify(s.sympify(P['raw_finite_difference_units'][key])-want)==s.simplify(s.sympify(R['raw_finite_difference_units'][key])-want)==0
assert P['radial_residues']==['1']*6
h,d=s.symbols('h d');ref=P['reference_raw_angular_polynomial'];anti=P['reference_conjugate_raw_polynomial']
for key in expected:
 assert s.degree(s.together(s.sympify(ref[key])*d*(d+2)),h)<=2
 assert s.simplify(s.sympify(anti[key])-(1 if key.startswith('E') else -1)*s.sympify(ref[key]))==0
for key,v in P['pure_Yukawa_paths'].items():
 kind,j,roles=key.split('_');assert v==R['pure_Yukawa_formal_roles'][roles]
assert P['pure_Yukawa_finite_difference']==R['pure_Yukawa_finite_difference']=='0_BY_CHECKED_CHIRAL_PATH_AND_BOUND_FULL_POLARIZATION'
for obj in [P,R]:assert obj['full_internal_hat_gauge_and_scalar_current_vertices'] and obj['widths_symbolic'] and obj['general_family_extension']=='Y_R tensor B_R_NO_TRACE_NO_EXTRA3' and not obj['physical_scheme_or_finite_parameter_counterterm_adopted'] and obj['new_two_loop_integrals']==0
C=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');Bs=[dec(C[k]) for k in ['B10','B126']];G=packed(CAL/'canonical_so10_gauge_yukawa_vertex_poles/primary_tables.json.gz');CI,CH=map(dec,G['fermion_Casimir_I_H']);CW=WM*CI+(WH-WM)*CH;I=s.eye(16)
swap=s.SparseMatrix(256,256,{(16*i+j,16*j+i):1 for i in range(16) for j in range(16)})
nonzero=[];mismatchcollapse=[];uniform=[]
for rr,B in enumerate(Bs):
 pp=P['models'][rr];qq=R['models'][rr];maps={k:dec(v) for k,v in pp.items()}
 for k in ['exchange','scalar_left','scalar_right','total']:z(maps[k]-dec(qq[k]))
 ji=dec(G['models'][rr]['J_I']);jh=dec(G['models'][rr]['J_H']);jw=WM*ji+(WH-WM)*jh
 ei=-4*ji-s.Rational(5,6)*(jw-ji)
 li=s.kronecker_product(CI.T,I)*B+ji;ri=s.kronecker_product(I,CI.T)*B+ji;lw=s.kronecker_product(CW.T,I)*B+jw;rw=s.kronecker_product(I,CW.T)*B+jw
 z(maps['exchange']-ei);z(maps['scalar_left']-li/2-s.Rational(5,6)*(lw-li));z(maps['scalar_right']-ri/2-s.Rational(5,6)*(rw-ri))
 z(maps['total']-sum((maps[k] for k in ['exchange','scalar_left','scalar_right']),s.zeros(256,328)))
 z(swap*maps['exchange']-maps['exchange']);z(swap*maps['scalar_left']-maps['scalar_right']);z(swap*maps['total']-maps['total'])
 z(maps['total']+s.Rational(23,6)*ji-s.Rational(5,6)*jw+(s.kronecker_product(CI.T,I)+s.kronecker_product(I,CI.T))*B/3-s.Rational(5,6)*(s.kronecker_product(CW.T,I)+s.kronecker_product(I,CW.T))*B)
 complement=list(range(54))+[326,327];z(maps['total'][:,complement])
 # Incorrect early W*k collapse changes only mixed longitudinal units.
 bad=ei+li/2+(lw-li)/2+ri/2+(rw-ri)/2
 remainder=(maps['total']-bad).applyfunc(s.expand);assert s.SparseMatrix(remainder).todok();mismatchcollapse.append(len(s.SparseMatrix(remainder).todok()))
 z(remainder.subs({WH:1,WM:1}));uniform.append('WIDTH_ONE_CONTROL_INSENSITIVE_ONLY')
 assert any(v.has(WH) or v.has(WM) for v in maps['total'].todok().values())
 nonzero.append({k:len(s.SparseMatrix(v).todok()) for k,v in maps.items()})
assert s.sympify(R['wrong_premature_width_collapse_longitudinal_unit'])==-s.I/2
YPP=packed(CAL/'canonical_so10_yukawa_polarization_poles/primary_tables.json.gz')
for row in YPP['unconjugated_sums']:z(dec(row))
for row in YPP['conjugated_projectors']:assert s.SparseMatrix(dec(row)).todok()
controls={'premature_actual_width_contraction':all(mismatchcollapse),'drop_either_scalar_branch':all(r['scalar_left'] and r['scalar_right'] for r in nonzero),
 'retain_two_independent_widths':all(r['total'] for r in nonzero),'wrong_mixed_branch_phase':all(r['scalar_left'] for r in nonzero),
 'open_half_family3_or_complex_scalar_half':all(r['exchange'] for r in nonzero),'full_internal_hat_reference_vertices':any(s.sympify(v).has(h) for v in ref.values()),
 'replace_unconjugated_zero_by_conjugated_tensor':all(bool(dec(v).todok()) for v in YPP['conjugated_projectors'])}
assert all(controls.values()) and digest(ROOT/'project_state.json')=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
print('RESULT '+json.dumps({'status':'QUALIFIED_COMPLETE_MARGINAL_FINITE_PROPER_YUKAWA_VERTEX_COMPARISON','elapsed_after_imports':time.perf_counter()-start,
 'oriented_gauge_diagram_units':3,'finite_proper_families_including_pure_Yukawa':4,'model_diagram_positions_compared':2*3*256*328,'total_map_positions_compared':2*256*328,'zero_complements_compared':True,
 'raw_finite_difference_units':P['raw_finite_difference_units'],'exchange':'-4*J_I-(5/6)*(J_W-J_I)','scalar_left':'(1/2)*Pleft_I+(5/6)*(Pleft_W-Pleft_I)','scalar_right':'(1/2)*Pright_I+(5/6)*(Pright_W-Pright_I)',
 'pure_Yukawa_finite_difference':'0_IN_THIS_LOCAL_COMPARISON','mass_symmetry_and_branch_transpose_remainder':'0','nonzero_positions':nonzero,
 'premature_width_collapse_changed_positions':mismatchcollapse,'width_one_collapse_control_insensitive':True,'controls':controls,
 'general_family_extension':'LINEAR_GENERAL_SYMMETRIC_Y_R_NO_TRACE_NO_EXTRA3','new_one_loop_finite_gauge_Yukawa_diagrams':3,'new_two_loop_integrals':0,
 'finite_parameter_counterterm_or_full_source_Slavnov_measure_phase_massive_matching_qualified':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','scientific_authority_changed':False,'authority':'34/39'},sort_keys=True),flush=True)
