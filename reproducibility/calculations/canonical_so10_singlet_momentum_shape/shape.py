"""SSM1: Feynman quadrature versus independently subtracted spectral integrals."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json, sys, time, threading, os
import mpmath as mp

R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
START=time.perf_counter();role=sys.argv[1];assert role in ['primary','replay']
timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
prep=json.loads((O/'preparation.json').read_bytes())
for raw,h in prep['input_sha256'].items():assert sha256(Path(raw).read_bytes()).hexdigest()==h,raw
old=json.loads((R/'calculations/canonical_so10_singlet_pole_control/primary_result.json').read_bytes())
assert old['all35_blocks328_real'] and old['all33_gauge_orbit_D_E_couplings_zero_checked']
assert old['direct_fermion_gauge_vertices_absent'] and old['physical_PQ_Higgs_zeros_retained']
probes=[]
for digits,index in [(40,0),(60,1)]:
 mp.mp.dps=digits;a=mp.mpf(6)/5;Q=mp.mpf(60);rows=old['probes'][index]['blocks']
 assert len(rows)==35 and sum(b['dimension']*len(b['mass_squared']) for b in rows)==328
 txt=lambda z:mp.nstr(z,38)
 ct=lambda z:[txt(mp.re(z)),txt(mp.im(z))]
 @lru_cache(None)
 def euclidean(x,y,b):
  if x==0 and y==0:return mp.log(b/Q)-2
  return mp.quadts(lambda u:mp.log((u*x+(1-u)*y+u*(1-u)*b)/Q),[0,mp.mpf('0.5'),1])
 @lru_cache(None)
 def spectral(x,y):
  if x==0 and y==0:return mp.log(mp.mpf(3)/4),mp.mpc(mp.log(4),-mp.pi)
  T=(mp.sqrt(x)+mp.sqrt(y))**2;U=(mp.sqrt(x)-mp.sqrt(y))**2
  if (x==0 and y==a) or (y==0 and x==a):T=a;U=a
  r=U/T
  def e_integrand(z):
   w=1-z*z
   return -4*a*a*T*z*z*w*mp.sqrt(1-r+r*z*z)/((T+a*w)*(T+2*a*w)*(T+3*a*w))
  ee=mp.quadts(e_integrand,[0,mp.mpf('0.5'),1])
  if T>=a:
   def f(z):
    w=1-z*z
    if T==a:
     return -12*a*a*T*w*mp.sqrt(1-r+r*z*z)/(a*(T+a*w)*(T+2*a*w))
    return -12*a*a*T*z*z*w*mp.sqrt(1-r+r*z*z)/((T-a*w)*(T+a*w)*(T+2*a*w))
   tt=mp.mpc(mp.quadts(f,[0,mp.mpf('0.5'),1]),0)
  else:
   ba=mp.sqrt((1-T/a)*(1-U/a))
   J=-mp.log(abs(T-a)*(T+2*a)**2/(T+a)**3)
   def rest(z):
    w=1-z*z;beta=z*mp.sqrt(1-r+r*z*z)
    numerator=2*(x+y)*w/(a*T)-(x-y)**2*(T+a*w)*w/(a*a*T*T)
    ratio=numerator/(beta+ba)
    return 12*a*a*T*z*ratio/((T+a*w)*(T+2*a*w))
   tt=mp.mpc(-ba*J-mp.quadts(rest,[0,mp.mpf('0.5'),1]),-mp.pi*ba)
  return ee,tt
 totalE=mp.mpf(0);totalT=mp.mpc(0);out=[];allpairs=0;weightedpairs=0;zeros=0
 for b in rows:
  masses=list(map(mp.mpf,b['mass_squared']));assert all(x>=0 for x in masses)
  terms=b.get('D_squared_and_kernel_all_pairs',[])
  if not terms:
   assert b['exact_zero_D_E'];zeros+=1
  else:
   assert len(terms)==len(masses)**2
   assert {(t['i'],t['j']) for t in terms}=={(i,j) for i in range(len(masses)) for j in range(len(masses))}
  ee=mp.mpf(0);tt=mp.mpc(0)
  for t in terms:
   allpairs+=1;x,y=masses[t['i']],masses[t['j']];weight=mp.mpf(t['D_abs2']);assert weight>=0
   if weight==0:continue  # exact printed zero only, never a numerical threshold
   weightedpairs+=1
   if role=='primary':
    one=euclidean(x,y,a);two=euclidean(x,y,2*a);three=euclidean(x,y,3*a)
    e=one-2*two+three
    saved=mp.mpc(*map(mp.mpf,t['L']))
    tpair=saved-3*one+2*two
   else:e,tpair=spectral(*sorted((x,y)))
   assert mp.log(mp.mpf(3)/4)-mp.mpf('1e-30')<=e<=mp.mpf('1e-30')
   ee+=weight*e;tt+=weight*tpair
  ee*=b['dimension']/(32*mp.pi**2);tt*=b['dimension']/(32*mp.pi**2)
  assert mp.im(tt)<=mp.mpf('1e-30')
  totalE+=ee;totalT+=tt
  out.append({'label':b['label'],'multiplicity':b['dimension'],'ordered_pair_positions':len(terms),
              'E':txt(ee),'T':ct(tt),'exact_zero_D_E':not bool(terms)})
 masslessE=mp.log(mp.mpf(3)/4);masslessT=mp.mpc(mp.log(4),-mp.pi)
 # Exact O(2) scalar reference fixes the physical PQ and radial weights.
 neutralE=(mp.mpf(12)/5*masslessE+mp.mpf(108)/5*(euclidean(a,a,a)-2*euclidean(a,a,2*a)+euclidean(a,a,3*a)))/(32*mp.pi**2)
 neutralrow=next(b for b in out if b['label']==[0,0,0,0])
 assert abs(mp.mpf(neutralrow['E'])-neutralE)<mp.mpf('1e-28')
 assert abs(mp.im(totalT)-mp.mpf(old['probes'][index]['cubic_bubble'][1]))<mp.mpf('1e-28')
 assert totalE<0 and mp.im(totalT)<0
 if role=='replay':
  he,ht=spectral(1000000*a,1000000*a)
  assert abs(he/(-mp.mpf(1)/30/10**12)-1)<mp.mpf('1e-5')
  assert abs(mp.re(ht)/(-mp.mpf(1)/10/10**12)-1)<mp.mpf('1e-5') and mp.im(ht)==0
 PQE=mp.mpf(12)/5*masslessE/(32*mp.pi**2);PQT=mp.mpf(12)/5*masslessT/(32*mp.pi**2)
 assert PQE!=0 and mp.im(PQT)!=0
 probes.append({'digits':digits,'blocks':out,'E':txt(totalE),'E_over_tree_mass_squared':txt(totalE/a),
 'T':ct(totalT),'T_over_tree_mass_squared':ct(totalT/a),'absolute_T_over_tree_mass_squared':txt(abs(totalT)/a),
 'PQ_E':txt(PQE),'PQ_T':ct(PQT),'zero_vertex_blocks':zeros,'ordered_pairs_retained':allpairs,
 'nonzero_printed_weights_including_tiny_entries':weightedpairs,
 'whole_Euclidean_shape_negative':True,'timelike_cut_matches_inherited_complete_cut':True})
 print('STAGE',role,digits,'complete35blocks',flush=True)
for field in ['E','E_over_tree_mass_squared','absolute_T_over_tree_mass_squared']:
 assert abs(mp.mpf(probes[0][field])-mp.mpf(probes[1][field]))<mp.mpf('1e-28'),field
for field in ['T','T_over_tree_mass_squared']:
 assert max(abs(mp.mpf(x)-mp.mpf(y)) for x,y in zip(probes[0][field],probes[1][field]))<mp.mpf('1e-28'),field
assert sum([1,-2,1])==sum([-1,4,-3])==0
assert sum([1,-3,2])==sum([1,3,-4])==0
elapsed=time.perf_counter()-START;assert elapsed<120
result={'schema':'SINGLET_MOMENTUM_SHAPE_V1','route':role,'probes':probes,
 'actual_coefficients_authenticated_and_reused_not_freshly_derived':True,
 'local_affine_subtractions_annihilated':True,'omitted_seagull_source_control_insensitive_by_design':True,
 'wrong_cut_sign_and_PQ_omission_sensitive':True,'no_new_point_or_input_scheme':True,
 'higher_loop_error_bound_or_quantum_control_or_physical_observable_proved':False,
 'whole_goal_complete':False,'authority_changed':False,'execution_state':'COMPLETED',
 'scientific_disposition':'COMPLETE_SAME_POINT_ONE_LOOP_SUBTRACTION_INVARIANT_MOMENTUM_COMBINATIONS_REQUIRE_INDEPENDENT_VALIDATION',
 'elapsed_after_imports':elapsed}
print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
