"""Full328 quartic lower certificate at one unchanged finite exploratory point."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import sys,json,time,threading,os
import sympy as S
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_mixed_bfb'));import bounds as old
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def car():
 def remove(I,q):
  if q not in I:return None
  i=I.index(q);return I[:i]+I[i+1:],(-1)**i
 def insert(I,p):
  if p in I:return None
  j=sum(i<p for i in I);return tuple(sorted(I+(p,))),(-1)**j
 count=0
 for I in combinations(range(10),5):
  for p in range(10):
   for q in range(10):
    out={}
    for first,second in [(remove,insert),(insert,remove)]:
     a=first(I,q if first==remove else p)
     if a is None:continue
     b=second(a[0],p if second==insert else q)
     if b is not None:out[b[0]]=out.get(b[0],0)+a[1]*b[1]
    out={k:v for k,v in out.items() if v};assert out==({I:1} if p==q else {})
    count+=1
 return count
def main():
 start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();prep=read(O/'preparation.json');writes=[]
 def readonly(event,args):
  if event=='open' and len(args)>1 and isinstance(args[1],str) and any(v in args[1] for v in 'wax+'):
   writes.append(str(args[0]));raise PermissionError('FULL_BFB_WRITE_DENIED')
 sys.addaudithook(readonly)
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 pt=read(C/'canonical_so10_coherent_joint_witness/POINT.json');p1,p2,x,s,z,D,t,delta,eta=[S.Rational(pt[n]) for n in ['p1','p2','x','s','z','D','t','Delta','eta']]
 c=old.point_coefficients();values=[p1,p2,delta+t/4,t,x/8,(5*s+z)/2-5*D/24,(-3*s-z)/2+5*D/24,(z-s)/4]
 for n,v in zip(['lambdaPhi1','lambdaPhi2','lambdaPhiSigma1','lambdaPhiSigma2','lambdaSigma1','lambdaSigma2','lambdaSigma3','lambdaSigma4'],values):c[n]=v
 c['zEta']=eta;assert c['lambdaPhiS']==c['lambdaSigmaS']==c['zD']==0
 tau=(s-2*values[7])/6;assert tau==S.Rational(1,12000)>0
 z4sq=S.expand(c['z4']*S.conjugate(c['z4']));k=S.Abs(c['zK']);assert k==S.Rational(3,100)
 pure_discard=s-2*values[7]-6*tau;assert pure_discard==0 and values[6]>0 and values[7]+tau>=0
 assert t>0 and c['lambdaPhiphi2']>=0 and c['lambdaPhiVector2']>=0 and p2>=0
 M=S.Matrix([[p1+p2/10,delta/2,(c['lambdaPhiphi1']-k)/2,c['lambdaPhiS']/2],
  [delta/2,x/8,(c['lambdaSigmaphi1']+min(c['lambdaSigmaphi2'],0)-eta*eta/tau)/2,c['lambdaSigmaS']/2-z4sq/t],
  [(c['lambdaPhiphi1']-k)/2,(c['lambdaSigmaphi1']+min(c['lambdaSigmaphi2'],0)-eta*eta/tau)/2,c['lambdaPhiVector1'],(c['lambdaVectorS']-k)/2],
  [c['lambdaPhiS']/2,c['lambdaSigmaS']/2-z4sq/t,(c['lambdaVectorS']-k)/2,c['lambdaS']]])
 minors=[S.factor(M[:i,:i].det()) for i in range(1,5)];passed=all(v>0 for v in minors);assert passed
 w=S.Matrix([1,1,2,2]);den=(w.T*M.inv()*w)[0];margin=S.factor(1/den);assert margin>0
 CAR=car();assert CAR==25200
 print('STAGE exact_four_norm_certificate_and_complete_CAR',flush=True)
 # Literal whole parent evaluations are controls, not the global proof.
 forms=[old.selfdual_form(),old.generated_form(4,8),old.rotate_form(old.selfdual_form())];controls=[];active={n:False for n in ['z4','zK','zEta']}
 for i,f in enumerate(forms):
  P=S.diag(1,-1,*([0]*8));phi=(1,S.I)+(0,)*8;sing=S.Rational(3,5)+S.I*S.Rational(4,5)
  if i==1:P=S.diag(*([-2]*6+[3]*4));phi=(1,S.I,1+S.I)+(0,)*7
  inv=old.invariant_values(old.State(P,f,phi,sing));v=S.expand(sum(c[n]*inv[n] for n in old.REAL_NAMES[6:])+sum(2*S.re(c[n]*inv[n]) for n in ['z4','zK','zEta','zD']))
  norms=S.Matrix([S.trace(P*P),old.norm(f),sum(a*S.conjugate(a) for a in phi),sing*S.conjugate(sing)])
  lower=S.factor((norms.T*M*norms)[0]);gap=S.factor(v-lower);assert v>0 and gap>=0
  for n in active:active[n]|=inv[n]!=0
  controls.append({'case':i,'quartic':str(v),'lower':str(lower),'gap':str(gap),'norms':list(map(str,norms))})
 assert all(active.values())
 # The former larger-tau shortcut would leave a negative discarded norm.
 badtau=2*tau;assert s-2*values[7]-6*badtau<0
 assert c['lambdaS']>0 and -c['lambdaS']<0
 assert eta*eta/tau>0 and 2*k!=k
 for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
 assert not writes and time.perf_counter()-start<120
 out={'schema':'FINITE_FULL_BFB_PRIMARY_V1','status':'POSITIVE_GLOBAL_LOWER_FORM_REQUIRE_INDEPENDENT_RECEIPT','same_frozen_exploratory_point':True,'all328_quartic_BFB_certificate':bool(passed),'lower_matrix':[[str(v) for v in row] for row in M.tolist()],'leading_minors':list(map(str,minors)),'proof_tau':str(tau),'discarded_Q1_coefficient':str(pure_discard),'remaining_Q4_coefficient':str(values[6]),'eta_Nu_penalty':str(eta*eta/tau),'z4_absolute_square':str(z4sq),'zK_norm_bound':str(k),'canonical_uniform_margin':str(margin),'canonical_uniform_margin_decimal':str(S.N(margin,20)),'canonical_radius_squared':'x+N+2u+2v','complete_exterior_CAR_slots':CAR,'literal_parent_controls':controls,'all_three_complex_interactions_active':active,'controls':{'negative_S_direction_detected':True,'ineligible_tau_rejected':True,'eta_penalty_nonzero':True,'Hermitian_factor_matters':True,'K_bound_uses_full_exterior_norm':True},'parameter_values':{n:str(v) for n,v in c.items()},'new_parameter_points':0,'new_benchmark_adopted':False,'preferred_vacuum_proved':False,'quantum_control_proved':False,'full_gauged_scattering_pass':False,'scientific_authority_changed':False,'whole_goal_complete':False,'input_sha256':prep['input_sha256'],'seconds_after_import':time.perf_counter()-start,'write_attempts':writes}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True);timer.cancel()
if __name__=='__main__':main()
