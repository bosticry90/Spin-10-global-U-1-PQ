"""Separate SSM1 verifier: elementary log primitives, no native imports."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import json,time,subprocess,threading,os
import mpmath as mp
T0=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
R=Path('C:/Users/psboy/Documents/ToE-Next');O=R/'calculations/canonical_so10_singlet_momentum_shape'
p=json.loads((O/'validation_preparation.json').read_bytes())
for raw,h in p['input_sha256'].items():assert sha256(Path(raw).read_bytes()).hexdigest()==h,raw
prep=json.loads((O/'preparation.json').read_bytes())
for b in prep['historical_git_bindings']:
 raw=subprocess.check_output(['git','show',b['commit']+':'+b['path']],cwd=R)
 assert sha256(raw).hexdigest()==b['sha256']
old=json.loads((R/'calculations/canonical_so10_singlet_pole_control/primary_result.json').read_bytes())
receipt=json.loads((R/'calculations/canonical_so10_singlet_pole_control/validation_receipt.json').read_bytes())
assert receipt['status']=='COMPLETED_FORMAL_ONE_LOOP_POLE_CORRECTION_EXCEEDS_TREE_MASS_SQUARED'
assert not receipt['physical_mass_width_or_input_adopted'] and not receipt['higher_order_error_bound']
assert old['all35_blocks328_real'] and old['fixed_parent_parameters_under_derivatives']
assert old['direct_fermion_gauge_vertices_absent'] and old['all33_gauge_orbit_D_E_couplings_zero_checked']
assert old['unknown_Phi_Sigma_shifts_multiply_zero_mass_derivatives']
mp.mp.dps=75;a=mp.mpf(6)/5;Q=mp.mpf(60);tol=mp.mpf('1e-28')
def plog(x):return mp.mpf(0) if x==0 else x*mp.log(abs(x))
def froot(r):return plog(1-r)+plog(r)-1
def Euclidean(x,y,b):
 discriminant=mp.sqrt((b+x-y)**2+4*b*y)
 lo=(b+x-y-discriminant)/(2*b);hi=(b+x-y+discriminant)/(2*b)
 if y==0:lo=mp.mpf(0)
 if x==0:hi=mp.mpf(1)
 assert lo<=0 and hi>=1
 return mp.log(b/Q)+froot(lo)+froot(hi)
def timelike(x,y,s):
 linear=x-y-s;disc=linear**2-4*s*y
 if disc>=0:
  low=(-linear-mp.sqrt(disc))/(2*s);high=(-linear+mp.sqrt(disc))/(2*s)
  cut=max(mp.mpf(0),min(1,high)-max(0,low))
  return mp.mpc(mp.log(s/Q)+froot(low)+froot(high),-mp.pi*cut)
 middle=-linear/(2*s);radius=mp.sqrt(-disc)/(2*s)
 primitive=lambda z:z*mp.log(z*z+radius*radius)-2*z+2*radius*mp.atan(z/radius)
 return mp.mpc(mp.log(s/Q)+primitive(1-middle)-primitive(-middle),0)
def kernels(x,y):
 l1,l2,l3=[Euclidean(x,y,k*a) for k in [1,2,3]]
 return l1-2*l2+l3,timelike(x,y,a)-3*l1+2*l2

masslessE,masslessT=kernels(0,0)
assert abs(masslessE-mp.log(mp.mpf(3)/4))<mp.mpf('1e-65')
assert abs(masslessT-mp.mpc(mp.log(4),-mp.pi))<mp.mpf('1e-65')
heavyE,heavyT=kernels(1000000*a,1000000*a)
assert abs(heavyE/(-mp.mpf(1)/30/10**12)-1)<mp.mpf('1e-5')
assert abs(mp.re(heavyT)/(-mp.mpf(1)/10/10**12)-1)<mp.mpf('1e-5') and mp.im(heavyT)==0
assert abs(mp.im(timelike(a/4,a/4,a)))==0

# Both point vectors annihilate constants and s, and do NOT annihilate s².
for points,co in [([-a,-2*a,-3*a],[1,-2,1]),([a,-a,-2*a],[1,-3,2])]:
 assert sum(co)==0 and sum(x*c for x,c in zip(points,co))==0
 assert sum(x*x*c for x,c in zip(points,co))!=0

computed=[];pairs=nonzeros=zero_blocks=0
for b in old['probes'][-1]['blocks']:
 m=list(map(mp.mpf,b['mass_squared']));assert all(x>=0 for x in m)
 terms=b.get('D_squared_and_kernel_all_pairs',[])
 if not terms:
  assert b['exact_zero_D_E'];zero_blocks+=1
 else:
  assert len(terms)==len(m)**2
  assert len({(z['i'],z['j']) for z in terms})==len(terms)
 E=mp.mpf(0);T=mp.mpc(0)
 for item in terms:
  pairs+=1;x,y=m[item['i']],m[item['j']];weight=mp.mpf(item['D_abs2']);assert weight>=0
  if weight!=0:nonzeros+=1
  e,t=kernels(x,y)
  assert mp.log(mp.mpf(3)/4)-tol<=e<=tol
  # Fresh analytic timelike integral checks inherited data, not the converse.
  recorded=mp.mpc(*map(mp.mpf,item['L']))
  assert abs(timelike(x,y,a)-recorded)<mp.mpf('1e-45')
  E+=weight*e;T+=weight*t
 normalization=mp.mpf(b['dimension'])/(32*mp.pi**2)
 computed.append((b['label'],E*normalization,T*normalization))
assert len(computed)==35 and pairs==157 and nonzeros==133 and zero_blocks==20
assert sum(b['dimension']*len(b['mass_squared']) for b in old['probes'][-1]['blocks'])==328
E=sum(x[1] for x in computed);T=sum(x[2] for x in computed)
assert E<0 and mp.im(T)<0
assert abs(mp.im(T)-mp.mpf(receipt['cubic_bubble'][1]))<tol

# Literal broken O(2) potential lambda*(h²+p²-v²)^2/4 gives these two cubics.
v=mp.sqrt(mp.mpf(3)/5);pq_weight=(2*v)**2;radial_weight=(6*v)**2
assert abs(pq_weight-mp.mpf(12)/5)<mp.mpf('1e-65')
assert abs(radial_weight-mp.mpf(108)/5)<mp.mpf('1e-65')
e_rad,t_rad=kernels(a,a)
neutralE=(pq_weight*masslessE+radial_weight*e_rad)/(32*mp.pi**2)
neutralT=(pq_weight*masslessT+radial_weight*t_rad)/(32*mp.pi**2)
actual_neutral=next(x for x in computed if x[0]==[0,0,0,0])
assert abs(actual_neutral[1]-neutralE)<tol and abs(actual_neutral[2]-neutralT)<tol
assert abs(pq_weight*mp.pi/(32*mp.pi**2)-mp.mpf(receipt['PQ_absorptive_mass_squared']))<tol
assert pq_weight*masslessE/(32*mp.pi**2)!=0
assert mp.im(T)!=-mp.im(T)  # wrong cut sign is sensitive

# Restore arbitrary local terms, including the actual complete pole's source.
local=mp.mpf(old['probes'][-1]['seagull'])+mp.mpf(old['probes'][-1]['vacuum_shift_insertion'])
for points,coeff in [([-a,-2*a,-3*a],[1,-2,1]),([a,-a,-2*a],[1,-3,2])]:
 assert abs(sum(c*(local+1234-567*s) for s,c in zip(points,coeff)))<mp.mpf('1e-65')
# Seagull/source omission is INSENSITIVE; no pole-completeness inference.

# Read native results only after independent analytic calculation.
native_times={}
for role in ['primary','replay']:
 cap=json.loads((O/(role+'_capture.json')).read_bytes())
 assert cap['execution_state']=='COMPLETED' and not cap['failed_or_incomplete_counted_as_PASS']
 r=json.loads((O/(role+'_result.json')).read_bytes());native_times[role]=r['elapsed_after_imports'];assert native_times[role]<120
 assert not r['authority_changed'] and not r['whole_goal_complete']
 assert not r['higher_loop_error_bound_or_quantum_control_or_physical_observable_proved']
 for q in r['probes']:
  assert len(q['blocks'])==35
  for row,(label,e,t) in zip(q['blocks'],computed):
   assert row['label']==label and abs(mp.mpf(row['E'])-e)<tol
   assert abs(mp.mpc(*map(mp.mpf,row['T']))-t)<tol
  assert abs(mp.mpf(q['E'])-E)<tol
  assert abs(mp.mpc(*map(mp.mpf,q['T']))-T)<tol
  assert abs(mp.mpf(q['E_over_tree_mass_squared'])-E/a)<tol
  assert abs(mp.mpf(q['absolute_T_over_tree_mass_squared'])-abs(T)/a)<tol
assert sha256((R/'project_state.json').read_bytes()).hexdigest()=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
assert sum(f.stat().st_size for f in O.iterdir() if f.is_file())<4*1024**2
elapsed=time.perf_counter()-T0;assert elapsed<180
text=lambda x:mp.nstr(x,32)
out={'schema':'SINGLET_MOMENTUM_SHAPE_VALIDATION_V1','execution_state':'COMPLETED',
 'scientific_disposition':'QUALIFIED_COMPLETE_SAME_POINT_ONE_LOOP_AFFINE_SUBTRACTION_INDEPENDENT_SINGLET_MOMENTUM_COMBINATIONS_NOT_QUANTUM_CONTROL',
 'input_sha256':p['input_sha256'],'historical_git_bindings_checked':prep['historical_git_bindings'],
 'blocks':35,'real_directions':328,'ordered_pair_positions':pairs,'nonzero_printed_weights_retained':nonzeros,
 'zero_vertex_blocks':zero_blocks,'native_seconds_after_imports':native_times,'elapsed_after_imports':elapsed,
 'E':text(E),'E_over_tree_mass_squared':text(E/a),'T':[text(mp.re(T)),text(mp.im(T))],
 'T_over_tree_mass_squared':[text(mp.re(T)/a),text(mp.im(T)/a)],'absolute_T_over_tree_mass_squared':text(abs(T)/a),
 'independent_analytic_log_primitives_phase_space_and_all_block_comparison':True,
 'affine_local_terms_annihilated_not_set_zero':True,'seagull_source_omission_insensitive_disclosed':True,
 'actual_original_140percent_pole_warning_preserved':True,'physical_input_changed':False,
 'higher_order_error_bound_quantum_control_model_exclusion_or_E5_promotion':False,
 'failed_native_workers':0,'failed_verifier_workers':0,'authority_changed':False,'whole_goal_complete':False}
print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
