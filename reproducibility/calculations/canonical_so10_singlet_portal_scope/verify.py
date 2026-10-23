"""SPS1 exact support, finite provenance and adversarial normalization gate."""
from data import *
import sympy as s
start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
fields=['names','full_pole_terms','zero_portal_pole_terms','active_restricted_names','point_beta_I','independent_of_changed_quartics_and_eta','beta_I_equals_two_parameter_pole','new_loop_integrals']
for key in fields:assert A[key]==B[key],key
names=A['names'];assert len(names)==26 and B['matrix_positions_read']==1352
for n in PORTALS:
 # Compare all symmetric quadratic coefficient positions, including zeros.
 for i,a in enumerate(names):
  for b in names[i:]:
   key='*'.join(sorted((a,b)))
   assert F(A['full_pole_terms'][n].get(key,'0'))==F(B['full_pole_terms'][n].get(key,'0'))
assert [len(A['zero_portal_pole_terms'][n]) for n in PORTALS]==[6,4]
assert not set(CHANGED)&set(A['active_restricted_names'])
assert A['point_beta_I']['old']==A['point_beta_I']['finite']
assert all(F(v)>0 for v in A['point_beta_I']['finite'].values())
packet=CAL/'canonical_so10_finite_radial_control/primary_result.json';point='calculations/canonical_so10_coherent_joint_witness/POINT.json'
assert read(CAL/'canonical_so10_finite_radial_control/validation_receipt.json')['input_sha256'][point]==digest(ROOT/point)
receipts={label:read(CAL/folder/name) for label,folder,name in [
 ('RG','canonical_so10_singlet_pole_rg_check','validation_receipt.json'),
 ('pole','canonical_so10_singlet_pole_control','validation_receipt.json'),
 ('quartic','canonical_so10_singlet_quartic_running','validation_receipt.json'),
 ('source','canonical_so10_singlet_quartic_running','source_receipt.json')]}
for label,r in receipts.items():
 assert r['input_sha256']['calculations/canonical_so10_finite_radial_control/primary_result.json']==digest(packet),label
prior=read(CAL/'canonical_so10_singlet_pole_rg_check/primary_result.json')
for n in PORTALS:assert F(prior['beta_I'][n])==F(A['point_beta_I']['finite'][n]),n
assert receipts['RG']['status']=='COMPLETED_LOCAL_ONE_LOOP_POLE_RG_CANCELLATION_WITH_INDUCED_PORTALS'
assert receipts['pole']['status']=='COMPLETED_FORMAL_ONE_LOOP_POLE_CORRECTION_EXCEEDS_TREE_MASS_SQUARED'
# Exact controls are derived here without either native coefficient helper.
x,y,m,lam=s.symbols('x y m lam',real=True)
V=m*(x*x+y*y)/2+lam*(x*x+y*y)**2/4
U=s.expand(s.trace(s.hessian(V,(x,y))**2)/4)
assert s.expand(U-(m*m/2+4*lam*m*(x*x+y*y)/2+10*lam**2*(x*x+y*y)**2/4))==0
env={n:s.Symbol(n,real=True) for n in names}
controls={}
for n,rows in A['zero_portal_pole_terms'].items():
 expr=sum(s.Rational(c)*s.prod(env[v] for v in key.split('*')) for key,c in rows.items());assert expr!=0
 assert s.expand(expr.subs({env['z4_re']:env['z4_im'],env['z4_im']:-env['z4_re']},simultaneous=True)-expr)==0
 assert s.expand(expr.subs(env['z4_im'],0)-expr)!=0
 assert s.expand(expr.subs({env['z4_re']:0,env['z4_im']:0})-expr)!=0
 assert expr!=2*expr
 controls[n]={'wrong_beta_factor_rejected':True,'omitted_imaginary_z4_rejected':True,'changed_active_z4_detected':True,'z4_phase_rotation_preserved':True,'zero_generated_pole_rejected':True}
print('RESULT '+json.dumps({'status':'QUALIFIED_PORTAL_SUPPORT_AND_EXISTING_FINITE_SINGLET_SCOPE','elapsed_after_imports':time.perf_counter()-start,
 'full_symmetric_coefficient_positions':2*26*27//2,'raw_replay_matrix_positions':1352,'restricted_nonzero_terms':[6,4],
 'point_beta_I':A['point_beta_I'],'eight_quartics_and_complex_eta_absent_from_restricted_support':True,
 'existing_RG_result_already_at_finite_witness':True,'existing_large_singlet_pole_already_at_finite_witness':True,
 'finite_source_and_quartic_receipts_bound_to_same_packet':True,'O2_normalization_matches':True,'negative_controls':controls,
 'new_loop_integrals':0,'old_C1_threshold_transferred_to_finite_witness':False,'new_physical_inputs_or_benchmark':False,
 'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
