from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));H=lambda p:sha256(p.read_bytes()).hexdigest();tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'mass_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
g,xi,eta=s.symbols('g10 xi eta_H',real=True);l2,l3=s.symbols('L2 L3',real=True);loc={'g10':g,'xi':xi,'eta_H':eta};dec=lambda z:s.SparseMatrix(*z['shape'],{(i,j):s.sympify(v,locals=loc) for i,j,v in z['entries']});cl=lambda M:s.SparseMatrix(M).applyfunc(s.expand);enc=lambda M:{'shape':list(M.shape),'entries':[[int(i),int(j),str(v)] for(i,j),v in sorted(cl(M).todok().items()) if v]};Z=lambda m,n:s.SparseMatrix(m,n,{});flat=lambda M:s.SparseMatrix(256,1,lambda i,j:M[i//16,i%16]);unflat=lambda V:s.SparseMatrix(16,16,lambda i,j:V[i*16+j,0]);S=O.parent/'canonical_so10_intrinsic_scalar_source_ghost';Y=load(S/'yukawa_bridge_inputs.json.gz');TC=[cl(sum((dec(Y['RC'])[a,c]*dec(Y['Tminus'][a]) for a in range(45) if dec(Y['RC'])[a,c]),Z(16,16))) for c in range(45)];source=load(O/'primary_tables.json.gz');R=list(map(dec,load(O/'primary_inputs.json.gz')['scalar_representation']));Tvec=load(O/'primary_inputs.json.gz')['source_vectors'];IRR=read(O.parent/'canonical_so10_intrinsic_regulator_root_v2/review_receipt.json');IRS=read(O.parent/'canonical_so10_intrinsic_ghost_root_schur/assembly_receipt_v2.json');results=[];rp=0;up=0;residual=0;wrongtotal=0
def logs(M):
 return cl(M.applyfunc(lambda v:s.expand_log(v,force=True).expand().subs({s.log(2):l2,s.log(3):l3})))
for probe,z in enumerate(source['outputs']):
 maps={};T=dec(Tvec[probe]);RT=cl(s.SparseMatrix.hstack(*(rr*T for rr in R)))
 for label in ['B10','B126']:
  for anti in [False,True]:
   key=label+('_anti' if anti else'');B=dec(Y[label]).conjugate() if anti else dec(Y[label]);MT=cl(B*T);mm=unflat(MT);assert not cl(mm-mm.T).todok();variation=Z(256,45)
   for c in range(45):variation[:,c]=flat(cl(-s.I*g*(TC[c]*mm+mm*TC[c].T) if anti else s.I*g*(TC[c].T*mm+mm*TC[c])))
   assert not cl(variation+B*RT).todok(),(probe,key,'actual anti/holo covariance')
   q=IRR['local_model_results'][probe][label]['right' if anti else'left'];irroot=logs(dec(q['heat_regulator_root']));oldrelative=logs(dec(q['corrected_relative_minus_sole_FIS_lift']));known=IRS['results'][probe]['maps'][key]['finite_root_prime_logs'];rows={}
   for prime,L in [(2,l2),(3,l3)]:
    V=dec(z['prime_logs'][str(prime)]['V']);U=dec(z['prime_logs'][str(prime)]['U']);coef=-4 if prime==2 else 2;M=coef*MT;rho=cl(M-B*V);rhoactual=flat(irroot.applyfunc(lambda a:s.expand(a).coeff(L)));rhodiff=cl(rho+rhoactual);ordinary=coef*variation;uimage=cl(ordinary+B*U);actual=dec(known[str(prime)]);udiff=cl(uimage+actual)
    scalar_route=cl(B*(U-coef*RT));assert not cl(uimage-scalar_route).todok();rppos=256;uppos=256*45;rp+=rppos;up+=uppos;residual+=len(rhodiff.todok())+len(udiff.todok());wrongrho=cl(-M-B*V+rhoactual);wrongu=cl(-ordinary+B*U+actual);omitU=cl(ordinary+actual);wrongtotal+=len(wrongrho.todok())+len(wrongu.todok())
    rows[str(prime)]={'relative_mass':enc(M),'rho_source_Euler':enc(-B*V),'rho_total':enc(rho),'rho_plus_measured_heat_root':enc(rhodiff),'u_ordinary_variation':enc(ordinary),'u_source_Euler':enc(cl(B*U)),'u_total':enc(uimage),'u_plus_measured_heat_root':enc(udiff),'wrong_old_mass_sign_rho_residual_positions':len(wrongrho.todok()),'wrong_old_mass_sign_u_residual_positions':len(wrongu.todok()),'omit_U_u_residual_positions':len(omitU.todok())}
    assert all(s.Poly(v,g,xi,eta) is not None for M0 in [M,V,U,rho,uimage] for v in M0.todok().values())
   combined=unflat(cl(dec(rows['2']['rho_total'])*l2+dec(rows['3']['rho_total'])*l3));assert not cl(combined+irroot).todok() and not cl(combined-oldrelative).todok();assert not dec(known['5']).todok()
   maps[key]={'prime_logs':rows,'relative_minus_sole_canonical_lift_mass':enc(combined),'actual_mass_symmetric':True,'direct_color_and_scalar_coordinate_variations_agree':True}
 results.append({'probe':probe,'maps':maps})
out={'schema':'IFC2_COMMON_LOCAL_SOURCE_MASS_CONVERSION','elapsed_after_imports':time.perf_counter()-tick,'rho_prime_positions_including_zeros':rp,'u_prime_positions_including_zeros':up,'residual_positions':residual,'wrong_old_mass_sign_total_residual_positions':wrongtotal,'results':results,'source_descendants_H_F_are_predictions_not_new_quantum_roots':True,'local_formal_conversion_constructed_in_three_measured_carriers':True,'Q_closed_restoration_counterterm_or_full_prescription':False,'physical_baselines_or_E5_A5_authority_changed':False}
with(O/'mass_precheck.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True)+'\n').encode())
assert residual==0
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
