"""SGH1 direct spectral recomputation versus analytic scaling/projector route."""
from pathlib import Path
from hashlib import sha256
import json,sys,time,threading,os
import sympy as s
import mpmath as mp
START=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;role=sys.argv[1]
assert role in ['primary','replay'];prep=json.loads((O/'preparation.json').read_bytes())
for raw,h in prep['input_sha256'].items():assert sha256(Path(raw).read_bytes()).hexdigest()==h,raw
read=lambda p:json.loads(p.read_bytes())
rad=read(R/'calculations/canonical_so10_finite_radial_control/primary_result.json')
bos=read(R/'calculations/canonical_so10_finite_radial_control/bosonic_primary_result.json')
pole=read(R/'calculations/canonical_so10_singlet_pole_control/primary_result.json')
rg=read(R/'calculations/canonical_so10_singlet_pole_rg_check/primary_result.json')
cache=read(R/'calculations/canonical_so10_singlet_tadpole/original_v2_result.json')
assert len(cache['slots'])==34 and len(cache['block_inputs'])==35
assert len(rad['raw_coefficients'])==29 and len([q for q in cache['slots'] if ':' in q])==10
H=s.Matrix(rad['exact_raw_radial_Hessian']);G=list(map(s.Rational,rad['radial_metrics']))
assert H==s.diag(*[H[i,i] for i in range(3)]) and all(H[i,i]>0 for i in range(3))
if role=='primary':
 geometry=[(s.Rational(b['gamma']),int(b['multiplicity']),[s.sympify(x)/2 for x in b['Gamma_derivative_trace'][:2]]) for b in bos['new_gauge_spectral_coefficients']]
else:
 old=read(R/'calculations/canonical_so10_radial_bosonic_tadpoles/original_v2_result.json')
 GP=s.SparseMatrix(old['gauge_Gamma_Phi']);GS=s.SparseMatrix(old['gauge_Gamma_Sigma']);GG=GP+GS
 assert GP*GS==GS*GP and GG==s.SparseMatrix(old['gauge_Gamma'])
 values=[s.S.Zero,s.Rational(3,5),s.Integer(3),s.Integer(50),s.Rational(253,5)];geometry=[]
 total=s.zeros(45)
 for gamma in values:
  P=s.eye(45)
  for other in values:
   if gamma!=other:P=P*(GG-other*s.eye(45))/(gamma-other)
  assert P*P==P and GG*P==gamma*P;total+=P
  if gamma!=0:geometry.append((gamma,int(s.trace(P)),[s.trace(P*GP),s.trace(P*GS)]))
 assert total==s.eye(45)
assert sum(n for _,n,_ in geometry)==33
assert [n for _,n,_ in geometry]==[8,1,12,12]
probes=[]
for digits in [50,80]:
 mp.mp.dps=digits;num=lambda x:mp.mpf(str(s.N(x,digits+10)));text=lambda x:mp.nstr(x,38)
 hh=[num(H[i,i]) for i in range(3)];gm=list(map(num,G));base=rad['probes'][-1]
 S0=[mp.mpf(x) for x in base['raw_linear_response']];B0=[mp.mpf(x) for x in base['B_raw']];T0=[mp.mpf(x) for x in base['T_raw']];b=[B0[i]/hh[i] for i in range(3)]
 assert all(v>0 for v in S0+b)
 def scalar(e):
  if role=='replay':return [e*(S0[i]-b[i]*mp.log(e)) for i in range(3)]
  T=[mp.mpf(0)]*3;zeros=positive=0
  for block in base['blocks']:
   masses=list(map(mp.mpf,block['mass_squared']));nz=block['zero_copies'];assert all(abs(x)<mp.mpf('1e-60') for x in masses[:nz])
   assert all(x>mp.mpf('1e-40') for x in masses[nz:]);zeros+=block['dimension']*nz;positive+=block['dimension']*(len(masses)-nz)
   for i in range(3):
    dd=list(map(mp.mpf,block['D_radial_in_mass_basis_diagonals'][i]))
    T[i]+=block['dimension']*sum((e*x)*(mp.log(e*x/60)-1)*(e*dd[j]) for j,x in enumerate(masses) if j>=nz)/(32*mp.pi**2)
  assert zeros==38 and positive==290
  return [-T[i]/(e*hh[i]) for i in range(3)]
 def V(g):
  return [3*g**4*sum(num(ga)*2*num(tr[i])*(mp.mpf(1)/3-mp.log(g*g*num(ga)/60)) for ga,n,tr in geometry)/(32*mp.pi**2*hh[i]) if i<2 else mp.mpf(0) for i in range(3)]
 def orbit(u,e):
  # Recompute the scaled potential-orbit derivatives, then divide by scaled H.
  tad=[]
  for i in range(3):
   val=sum(num(ga)*(e*hh[i]/gm[i]*num(tr[i])/num(ga))*(mp.log(u*num(ga)/60)-1) for ga,n,tr in geometry) if i<2 else 0
   tad.append(u*val/(32*mp.pi**2))
  return [-tad[i]/(e*hh[i]) for i in range(3)]
 eps=[mp.mpf(1),mp.mpf(1)/2,mp.mpf(1)/10,mp.mpf(1)/100]
 scalarrows=[]
 for e in eps:
  r=scalar(e);closed=[e*(S0[i]-b[i]*mp.log(e)) for i in range(3)]
  assert max(abs(x-y) for x,y in zip(r,closed))<mp.mpf('1e-28')
  scalarrows.append({'epsilon':text(e),'raw_scalar_response':list(map(text,r))})
 assert 2*S0[1]>3*b[1] and V(mp.mpf('.5'))[1]>S0[1]-b[1]
 # Monotonic V implies unique roots; different parameterizations in the two routes.
 def solve(target):
  if role=='primary':
   lo,hi=mp.mpf(0),mp.mpf(1)
   for _ in range(250):
    mid=(lo+hi)/2
    if V(mid)[1]<target:lo=mid
    else:hi=mid
   return (lo+hi)/2
  lo,hi=mp.mpf(0),mp.mpf(64)
  for _ in range(250):
   mid=(lo+hi)/2
   if V(mp.exp(-mid))[1]>target:lo=mid
   else:hi=mid
  return mp.exp(-(lo+hi)/2)
 rootV=solve(mp.mpf(1));rootAM=solve(1/(4*S0[1]));assert 0<rootAM<rootV<1
 grid=[]
 for g in [mp.mpf(1)/4,mp.mpf(1)/2,mp.mpf(1)]:
  vv=V(g)
  for u in [mp.mpf(1)/4,mp.mpf(1)/2]:
   oo=orbit(u,mp.mpf(1))
   for e in eps:
    rr=scalar(e);actual=[rr[i]+vv[i]/e+orbit(u,e)[i] for i in range(3)]
    assert max(abs(x-y) for x,y in zip(orbit(u,e),oo))<mp.mpf('1e-28')
    lower=2*mp.sqrt(S0[1]*vv[1])+oo[1]
    assert actual[1]>=lower-mp.mpf('1e-28')
    grid.append({'epsilon':text(e),'g_diagnostic':text(g),'u_xi_g2_diagnostic':text(u),
      'raw_bosonic_response':list(map(text,actual)),'Sigma_AM_lower_bound':text(lower),
      'raw_vector_response_at_epsilon1':list(map(text,vv)),'raw_orbit_response':list(map(text,oo))})
 # Complete S pole, including the required vacuum-source term and scale log.
 pp=pole['probes'][-1];delta=mp.mpc(*map(mp.mpf,pp['total_delta_pole_squared']))
 if role=='primary':
  logcoef=mp.mpf(0)
  for block in pp['blocks']:
   if block.get('exact_zero_D_E'):continue
   mm=list(map(mp.mpf,block['mass_squared']));ee=list(map(mp.mpf,block['E_in_mass_basis_diagonal']))
   logcoef+=block['dimension']*(sum(x*y for x,y in zip(mm,ee))+sum(mp.mpf(v['D_abs2']) for v in block['D_squared_and_kernel_all_pairs']))/(32*mp.pi**2)
  logcoef-=mp.mpf(18)/5*b[2]
 else:logcoef=-mp.mpf(rg['explicit_log_derivative_numeric'])/2
 assert abs(logcoef+mp.mpf(rg['explicit_log_derivative_numeric'])/2)<mp.mpf('1e-28')
 polerows=[]
 for e in eps:
  d=e*e*(delta+logcoef*mp.log(e))
  polerows.append({'epsilon':text(e),'complete_S_delta_mass2':[text(mp.re(d)),text(mp.im(d))],
    'absolute_delta_over_scaled_tree_mass2':text(abs(d)/(e*mp.mpf(6)/5))})
 assert abs(mp.mpf(polerows[0]['absolute_delta_over_scaled_tree_mass2'])-mp.mpf(pp['absolute_delta_over_tree_mass_squared']))<mp.mpf('1e-28')
 # Sensitive omission controls away from the identity, insensitive at epsilon1.
 e=mp.mpf('.1');assert max(abs(scalar(e)[i]-e*S0[i]) for i in range(3))>mp.mpf('1e-8')
 assert V(mp.mpf('.5'))[1]/e!=V(mp.mpf('.5'))[1]
 assert orbit(mp.mpf('.25'),e)[1]!=orbit(mp.mpf('.25'),e)[1]/e
 exact_lower=s.Rational(1,2)**4*sum(ga*2*tr[1] for ga,n,tr in geometry)/(32*10*H[1,1]);assert exact_lower>1
 probes.append({'digits':digits,'scalar_responses':scalarrows,'bosonic_grid':grid,'singlet_poles':polerows,
  'S_base':list(map(text,S0)),'b_log':list(map(text,b)),'vector_only_root_g':text(rootV),'AM_necessary_root_g':text(rootAM),
  'S_pole_log_epsilon_coefficient':text(logcoef),'g_half_exact_vector_lower_bound_using_pi2_lt10':str(exact_lower),
  'g_half_all_epsilon_weakening_monotonically_worsens_Sigma':True})
 print('STAGE',role,digits,'complete',flush=True)
for key in ['vector_only_root_g','AM_necessary_root_g','S_pole_log_epsilon_coefficient']:
 assert abs(mp.mpf(probes[0][key])-mp.mpf(probes[1][key]))<mp.mpf('1e-28')
elapsed=time.perf_counter()-START;assert elapsed<120
out={'schema':'SCALAR_GAUGE_HOMOTHETY_V1','route':role,'probes':probes,
 'geometry':[[str(ga),n,list(map(str,tr))] for ga,n,tr in geometry],
 'scalar_coefficient_directions_scaled':34,'tree_scalar_masses_contact_and_quartic_scale_linearly':True,
 'nonlinear_vacuum_or_RG_trajectory_solved':False,'new_benchmark_or_gauge_input_adopted':False,
 'fermion_cancellation_full_quantum_control_or_model_no_go_claimed':False,'authority_changed':False,
 'scientific_disposition':'COMPLETE_UNIFORM_SCALAR_FAMILY_KNOWN_BOSONIC_TRADEOFF_REQUIRE_INDEPENDENT_VALIDATION',
 'execution_state':'COMPLETED','elapsed_after_imports':elapsed}
print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
