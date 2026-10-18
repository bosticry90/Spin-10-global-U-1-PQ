"""Timelike one-loop singlet self-energy and tree-vacuum source insertion."""
from pathlib import Path
from hashlib import sha256
import sys,json,time,threading,os
import sympy as S
import mpmath as mp
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_higgs_neutral_valley'));import inputs as inp
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def kernel(s,x,y,Q=60):
 b=x-y-s;disc=b*b-4*s*y
 if disc>=0:
  root=mp.sqrt(disc);r1=(-b-root)/(2*s);r2=(-b+root)/(2*s)
  xl=lambda z:mp.mpf(0) if z==0 else z*mp.log(abs(z))
  f=lambda r:xl(1-r)+xl(r)-1
  cut=max(mp.mpf(0),min(mp.mpf(1),r2)-max(mp.mpf(0),r1))
  return mp.mpc(mp.log(s/Q)+f(r1)+f(r2),-mp.pi*cut)
 u=-b/(2*s);v=mp.sqrt(-disc)/(2*s)
 F=lambda z:z*mp.log(z*z+v*v)-2*z+2*v*mp.atan(z/v)
 return mp.mpc(mp.log(s/Q)+F(1-u)-F(-u),0)
def main():
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();prep=read(O/'preparation_v2.json');writes=[]
 def readonly(event,args):
  if event=='open' and len(args)>1 and isinstance(args[1],str) and any(t in args[1] for t in 'wax+'):
   writes.append(str(args[0]));raise PermissionError('SINGLET_POLE_WRITE_DENIED')
 sys.addaudithook(readonly)
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 scalar=read(C/'canonical_so10_finite_radial_control/primary_result.json');source=read(C/'canonical_so10_singlet_quartic_running/source_receipt.json');assert source['fermion_S_mass_derivative_zero_for_any_Yukawas'] and source['all_bosonic_S_additions_zero']
 cache=read(C/'canonical_so10_singlet_tadpole/original_v2_result.json');slots=cache['slots'];raw={n:S.sympify(v) for n,v in scalar['raw_coefficients'].items()};co=[S.im(raw[n]) if part=='im' else S.re(raw[n]) for q in slots for n,_,part in [q.partition(':')]]
 count=lambda sector:int(sector in ['S','SBar']);blocks=[]
 for bb in cache['block_inputs']:
  n=len(bb['metric']);M=S.zeros(n);D=S.zeros(n);E=S.zeros(n);DP=S.zeros(n);DS=S.zeros(n)
  for k,i,j,z in bb['raw_H34_sparse']:
   q=slots[k];name=q.partition(':')[0];p=inp.SDEG[name]-count(bb['sectors'][i])-count(bb['sectors'][j]);assert p>=0
   value=co[k]*S.sympify(z);M[i,j]+=value;D[i,j]+=p*value;E[i,j]+=p*(p-1)*value
   DP[i,j]+=value*(inp.PHI[name]-int(bb['sectors'][i]=='Phi')-int(bb['sectors'][j]=='Phi'))
   DS[i,j]+=value*(inp.RESCALE.get(name,(0,0))[0]-int(bb['sectors'][i] in ['Sigma','SigmaBar'])-int(bb['sectors'][j] in ['Sigma','SigmaBar']))
  if any(count(q) for q in bb['sectors']):
   ids=[i for i,q in enumerate(bb['sectors']) if count(q)];assert DP.extract(ids,ids).applyfunc(S.simplify)==DS.extract(ids,ids).applyfunc(S.simplify)==S.zeros(2)
  W=S.diag(*[1/S.sqrt(S.Rational(g)) for g in bb['metric']]);M=W*M*W;D=W*D*W/S.sqrt(S.Rational(3,5));E=W*E*W/S.Rational(3,5)
  M,D,E=[A.applyfunc(S.expand) for A in [M,D,E]]
  for role,A in [('mass',M),('cubic',D),('quartic',E)]:assert (A-A.H).applyfunc(S.simplify)==S.zeros(A.rows),('NON_HERMITIAN',bb['label'],role)
  blocks.append((bb,M,D,E))
 probes=[]
 for digits in [80,110]:
  mp.mp.dps=digits;num=lambda z:mp.mpc(str(S.N(S.re(z),digits+10)),str(S.N(S.im(z),digits+10)));real=lambda z:mp.re(num(z));text=lambda z:mp.nstr(mp.re(z),60);ct=lambda z:[text(mp.re(z)),text(mp.im(z))];mat=lambda A:mp.matrix([[num(z) for z in row] for row in A.tolist()]);s=mp.mpf(6)/5;Gs=mp.mpf(3)/5
  counts={'positive':0,'gauge':0,'PQ':0,'Higgs':0};seagull=mp.mpf(0);bubble=mp.mpc(0);tad=mp.mpf(0);records=[];gauge_max=mp.mpf(0);pq_weight=mp.mpf(0);active_blocks=0
  for bb,MS,DS,ES in blocks:
   M,D,E=map(mat,[MS,DS,ES]);assert max(abs(z) for A in [M,D,E] for z in A-A.H)<mp.mpf('1e-65');ev,U=mp.eighe(M);n=M.rows;tol=mp.mpf('1e-60');ev=[mp.mpf(0) if abs(v)<tol else v for v in ev];assert all(v>=0 for v in ev);zero=[i for i,v in enumerate(ev) if v==0];counts['positive']+=bb['dimension']*(n-len(zero));P0=mp.zeros(n)
   for i in zero:
    ui=U[:,i];P0+=ui*ui.H
   PPQ=mp.zeros(n);PH=mp.zeros(n)
   if bb['label']==[0,0,0,0]:
    PS=mp.diag([int(count(q)) for q in bb['sectors']]);PPQ=P0*PS;assert mp.norm(PPQ-PPQ.H)<tol and mp.norm(PPQ*PPQ-PPQ)<tol
    assert abs(mp.re(sum(PPQ[i,i] for i in range(n)))-1)<tol
   elif tuple(bb['label']) in [(0,0,1,-3),(0,0,1,3)]:PH=P0
   Pg=P0-PPQ-PH
   for name,P in [('gauge',Pg),('PQ',PPQ),('Higgs',PH)]:
    rank=mp.re(sum(P[i,i] for i in range(n)));assert abs(rank-mp.nint(rank))<tol;counts[name]+=bb['dimension']*int(mp.nint(rank))
   residual=max([abs(v) for v in D*Pg]+[abs(v) for v in E*Pg]+[mp.mpf(0)]);gauge_max=max(gauge_max,residual);assert residual<mp.mpf('1e-55')
   if bb['label']==[0,0,0,0]:pq_weight=mp.re(sum((PPQ*D*PPQ*D)[i,i] for i in range(n)));assert abs(pq_weight-mp.mpf(12)/5)<mp.mpf('1e-55')
   if not any(DS) and not any(ES):
    records.append({'label':bb['label'],'dimension':bb['dimension'],'mass_squared':list(map(text,ev)),'exact_zero_D_E':True});continue
   active_blocks+=1;dd=U.H*D*U;ee=U.H*E*U;localA=mp.mpf(0);localB=mp.mpc(0);localT=mp.mpf(0);pairs=[]
   for i,x in enumerate(ev):
    aval=mp.mpf(0) if x==0 else x*(mp.log(x/60)-1);localA+=mp.re(ee[i,i])*aval;localT+=mp.re(dd[i,i])*aval
    for j,y in enumerate(ev):
     weight=abs(dd[i,j])**2;L=kernel(s,x,y);localB+=weight*L;pairs.append({'i':i,'j':j,'D_abs2':text(weight),'L':ct(L)})
   seagull+=bb['dimension']*localA/(32*mp.pi**2);bubble+=bb['dimension']*localB/(32*mp.pi**2);tad+=bb['dimension']*localT/(32*mp.pi**2)
   records.append({'label':bb['label'],'dimension':bb['dimension'],'mass_squared':list(map(text,ev)),'D_squared_and_kernel_all_pairs':pairs,'E_in_mass_basis_diagonal':[text(ee[i,i]) for i in range(n)],'seagull':text(bb['dimension']*localA/(32*mp.pi**2)),'bubble':ct(bb['dimension']*localB/(32*mp.pi**2)),'tadpole_canonical':text(bb['dimension']*localT/(32*mp.pi**2))})
  assert counts=={'positive':290,'gauge':33,'PQ':1,'Higgs':4};assert abs(tad-mp.mpf(scalar['probes'][-1]['T_canonical'][2]))<mp.mpf('1e-55')
  delta_r=mp.mpf(source['complete_reference_linear_S_response']);insertion=mp.mpf(18)/5*delta_r;Pi=seagull+bubble;delta=Pi+insertion;pole=s+delta;assert mp.im(Pi)<0
  assert abs(kernel(s,0,0)-(mp.log(s/60)-2-1j*mp.pi))<mp.mpf('1e-60')
  pq_absorptive=pq_weight/(32*mp.pi);assert abs(pq_absorptive-s/(16*mp.pi))<mp.mpf('1e-55')
  probes.append({'precision':digits,'counts':counts,'active_blocks':active_blocks,'gauge_D_E_projector_residual':text(gauge_max),'seagull':text(seagull),'cubic_bubble':ct(bubble),'one_particle_irreducible_Pi':ct(Pi),'canonical_tadpole':text(tad),'vacuum_shift_insertion':text(insertion),'total_delta_pole_squared':ct(delta),'formal_pole_squared':ct(pole),'absolute_delta_over_tree_mass_squared':text(abs(delta)/s),'real_delta_over_tree_mass_squared':text(mp.re(delta)/s),'leading_width_over_tree_mass':text(-mp.im(delta)/s),'PQ_absorptive_mass_squared':text(pq_absorptive),'one_loop_correction_exceeds_tree_mass_squared':bool(abs(delta)>s),'formal_negative_real_pole_squared':bool(mp.re(pole)<0),'blocks':records})
  print('STAGE complete_singlet_pole_'+str(digits),flush=True)
 for name in ['one_particle_irreducible_Pi','total_delta_pole_squared','formal_pole_squared']:
  assert max(abs(mp.mpf(a)-mp.mpf(b)) for a,b in zip(probes[0][name],probes[1][name]))<mp.mpf('1e-50'),name
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 assert not writes and time.perf_counter()-start<120
 out={'schema':'SINGLET_POLE_PRIMARY_V1','status':'COMPLETE_FORMAL_ONE_LOOP_S_POLE_COEFFICIENT_REQUIRE_INDEPENDENT_RECEIPT','tree_pole_squared':'6/5','external_radial_metric':'3/5','all35_blocks328_real':True,'direct_fermion_gauge_vertices_absent':True,'all33_gauge_orbit_D_E_couplings_zero_checked':True,'physical_PQ_Higgs_zeros_retained':True,'unknown_Phi_Sigma_shifts_multiply_zero_mass_derivatives':True,'fixed_parent_parameters_under_derivatives':True,'probes':probes,'new_nonlinear_pole_or_vacuum_solve':False,'full_quantum_control_proved':False,'physical_pole_mass_prediction_adopted':False,'model_refuted':False,'new_parameter_points':0,'flavor_work_resumed':False,'scientific_authority_changed':False,'whole_goal_complete':False,'seconds_after_import':time.perf_counter()-start,'input_sha256':prep['input_sha256'],'write_attempts':writes}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True);timer.cancel()
if __name__=='__main__':main()
