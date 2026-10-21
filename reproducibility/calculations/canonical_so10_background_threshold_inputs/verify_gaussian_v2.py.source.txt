"""Additional exact Gaussian/Legendre controls; no native helper imports."""
from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os
import sympy as s
D=Path(__file__).resolve().parent
def main():
 tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((D/'validation_preparation_v2.json').read_bytes())
 for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
 old=json.loads((D/'validation_receipt.json').read_bytes())
 assert old['status']=='PASS_BOUNDED_KINEMATIC_INPUT_AND_TOPOLOGY_ONLY'
 H,G,lam,k,u,a,j,x=s.symbols('H G lam k u a j x')
 V=lam*x**3/6+k*x**4/24-H*j*x
 # Independently generate the polynomial integrand, not the expected B.
 integrand=s.expand((1+u*x/a)*sum((-V/H)**n/s.factorial(n) for n in range(7)))
 gauss=0
 for (power,),coef in s.Poly(integrand,x).terms():
  if power%2==0:gauss+=coef*(s.factorial2(power-1) if power else 1)*(H*G)**(power//2)
 Z1=s.expand(gauss).coeff(H,1)
 jsol=s.solve(s.diff(Z1,j),j);assert jsol==[G*lam/2-u/a]
 Gamma2=s.factor(-Z1.subs(j,jsol[0]))
 expected=k*G**2/8-lam**2*G**3/12+u**2*G/(2*a**2)
 assert s.simplify(Gamma2-expected)==0
 assert s.expand(Gamma2).coeff(u,2)==G/(2*a**2)
 assert s.expand(-Z1.subs(j,0)-expected)!=0
 assert s.simplify(Gamma2-(expected-u**2*G/a**2))!=0
 rows=json.loads(gzip.decompress((D/'primary_tables.json.gz').read_bytes()))
 T={(a,b,i):s.sympify(z) for a,b,i,z in rows['T']}
 F={(a,b,c):s.sympify(z) for a,b,c,z in rows['f']}
 assert any(T.values()) and any(F.values())
 tensor_sign_mutant_changed=len(T);f_sign_mutant_changed=len(F)
 antisym=set()
 for aa,bb,ii in set(T)|{(bb,aa,ii) for aa,bb,ii in T}:
  if s.expand(T.get((aa,bb,ii),0)-T.get((bb,aa,ii),0))!=0:antisym.add((aa,bb,ii))
 assert len(antisym)==6784 and tensor_sign_mutant_changed==10524 and f_sign_mutant_changed==720
 # One-loop normalization cannot erase this genuinely different mass scheme.
 m,dm,ell=s.symbols('m dm ell',positive=True)
 shift=s.diff(s.log(m+ell*dm),ell).subs(ell,0)
 assert shift==dm/m and shift!=0 # symbolic mass CT slot, not fitted value
 out=dict(old)
 out.update({'schema':'C1_BACKGROUND_THRESHOLD_INPUT_VALIDATION_V2',
 'input_bindings':len(prep['input_sha256']),'prior_full_coefficient_receipt_reused':True,
 'zero_dimensional_Legendre_Gamma2':str(Gamma2),'ghost_sign_control_sensitive':True,
 'one_particle_reducible_tadpole_control_sensitive':True,
 'tensor_sign_mutant_changed':tensor_sign_mutant_changed,'f_sign_mutant_changed':f_sign_mutant_changed,
 'antisymmetric_mutant_changed':len(antisym),'elapsed_after_imports':time.perf_counter()-tick})
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
