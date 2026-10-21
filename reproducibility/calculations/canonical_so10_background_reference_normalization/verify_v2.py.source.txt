"""BCR1 independent exact and high-precision checks; imports no native helper."""
from pathlib import Path
from hashlib import sha256
import json,time,threading,os,math
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'

def main():
 tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'validation_preparation_v2.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 a,b=[json.loads((O/(role+'_v2_result.json')).read_bytes()) for role in ['primary','replay']]
 for key in a:
  if key not in ['role','elapsed_after_imports','reference_Phi_shapes','finite_sigma_LL']:assert a[key]==b[key],key
 assert a['field_count']==a['source_count']==643 and a['background_count']==48
 assert a['affine_rules']==96 and a['BRST_derivative_rows']==180
 assert a['reference_determinant_retained'] and not a['physical_scheme_adopted'] and not a['full_E5_A5_proved']
 def mat(n,m,rows):return s.SparseMatrix(n,m,{(i,j):s.sympify(v) for i,j,v in rows})
 def zero(m):return all(s.simplify(v)==0 for v in m.values())
 GB=mat(45,45,a['GB']);D=mat(45,45,a['D']);F=mat(45,12,a['F'])
 assert zero(GB*D-mat(45,45,a['Qbeta_tensor'])) and zero(GB*F-mat(45,12,a['Wbeta_tensor']))
 assert zero(D.T*GB*F-mat(45,12,a['mixed_parameter_gradient_tensor']))
 assert GB.rank()==45 and F.rank()==12 and (D.T*GB*F).rank()==12
 # Recompute scalar normalization from physical ordered traces, not result counts.
 rec=json.loads((PK/'frozen_a10_physical_reconciliation/full_primary.json').read_bytes())
 for tag in ['Phi','Sigma','phi','S']:
  rs=rec['representation_matrices'][tag];rho=[{(i,j):s.sympify(v) for i,j,v in r['entries']} for r in rs]
  index=s.simplify(-sum(v*rho[0].get((j,i),0) for (i,j),v in rho[0].items()))
  assert index==s.sympify(a['scalar_indices'][tag])
  for k in range(45):
   diagonal=s.simplify(sum(v*v for v in rho[k].values()));assert diagonal==index
  hg=mat(12,12,a['actual_H_scalar_grams'][tag]);assert zero(hg-index*F.T*GB*F)
 phi=mat(12,12,a['actual_H_scalar_grams']['Phi']);assert phi.rank()==12
 # All source transpose identities from actual E3 coefficients, with independent maps.
 full=json.loads((PK/'frozen_a10_e5_full_hessian/primary.json').read_bytes())['retained_reference'];fields=full['field_order'];fset=set(fields)
 e3=json.loads((PK/'frozen_a10_e3_symmetry/primary.json').read_bytes())['operators']['Tb_geometric_and_transported']
 fieldmaps={};srcmaps={};g=s.Symbol('g10')
 for n,rows in e3.items():
  for row in rows:
   om=[w for w in row['word'] if w.startswith('omega')];ot=[w for w in row['word'] if not w.startswith('omega')]
   if '__' in om[0]:continue
   h=int(om[0][5:]);v=s.expand(s.sympify(row['coefficient'])).coeff(g)
   if n in fset:fieldmaps[(h,n,ot[0])]=v
   elif n.startswith('J'):srcmaps[(h,ot[0][1:],n[1:])]=-v
 assert set(fieldmaps)==set(srcmaps) and all(s.simplify(v-srcmaps[k])==0 for k,v in fieldmaps.items())
 assert any(fieldmaps.values()) and sum(a['source_nonzero_counts'])==len(srcmaps)
 assert all(set(row.values())=={'0'} for row in a['separate_block_traces'])
 # Check finite-sigma inverse by direct numerical/rational inversion, not native formula.
 for qv,wv,sv in [([1,2,-1,0],s.Rational(3,2),s.Rational(1,7)),([0,0,0,0],2,3),([2,0,1,-3],s.Rational(1,3),s.Rational(5,2))]:
  q=s.Matrix(qv);Q=(q.T*q)[0];w=s.sympify(wv);sig=s.sympify(sv)
  K=((Q+sig)*s.eye(4)-q*q.T).row_join(q).col_join((-q.T).row_join(s.Matrix([[w]])))
  direct=K.inv();bb=s.eye(4)/(Q+sig)+(w-1)*q*q.T/((Q+sig)*(Q+w*sig))
  candidate=bb.row_join(-q/(Q+w*sig)).col_join((q.T/(Q+w*sig)).row_join(s.Matrix([[sig/(Q+w*sig)]])))
  assert direct==candidate and direct[4,4]!=0
  wrong=candidate.copy();wrong[4,4]=0;assert K*wrong!=s.eye(5)
 # Infrared auxiliary component is uniformly bounded and vanishes distributionally.
 # sigma/(Q+w sigma)<=1/w, tending0 off Q=0; no inverse-sigma partial fractions.
 Q,w,sig=s.symbols('Q w sigma',positive=True)
 assert s.simplify(1/w-sig/(Q+w*sig))==Q/(w*(Q+w*sig))
 assert s.limit(sig/(Q+w*sig),sig,0,dir='+')==0
 # Independent convergent beta-moment series with explicit entire tail bound.
 mp.mp.dps=90;shape_results=[];terms=[]
 for z in [1,2,3]:
  partial=mp.mpf('0');In=mp.mpf(1)/3;n=0
  while True:
   n+=1;In*=mp.mpf(n)/(2*(2*n+3));term=(-1)**n*mp.mpf(z)**n*In/n;partial+=term
   nextI=In*mp.mpf(n+1)/(2*(2*n+5));nextterm=mp.mpf(z)**(n+1)*nextI/(n+1)
   tail=nextterm/(1-mp.mpf(z)/4)
   if tail<mp.mpf('1e-75'):break
  assert n<10000
  for result in [a,b]:
   value=mp.mpf(dict(result['reference_Phi_shapes'])[z]);assert abs(value-partial)<mp.mpf('1e-25')
  assert partial<0;shape_results.append([z,mp.nstr(partial,70),mp.nstr(tail,5)]);terms.append(n)
 u=s.Symbol('u');moments=[]
 for n in range(9):
  # Polynomial expansion gives an independent rational integration route.
  poly=s.Poly(s.expand((1-2*u)**2*u**n*(1-u)**n),u)
  value=sum(c/s.Rational(p[0]+1) for p,c in poly.terms());assert value==s.sympify(a['scalar_moments'][n]);moments.append(str(value))
 assert moments[0]=='1/3' and moments[1]=='1/30'
 # Direct Feynman-parameter boundary identity for the full seagull+bubble.
 mp.mp.dps=90;ward_checks=[]
 for dim in [mp.mpf('1.5'),mp.mpf('3'),mp.mpf('3.8')]:
  mass=mp.mpf('1.7');z=mp.mpf('2.3')
  i1=lambda d:mp.gamma(1-dim/2)*d**(dim/2-1)
  i2=lambda d:mp.gamma(2-dim/2)*d**(dim/2-2)
  delta=lambda v:mass+v*(1-v)*z
  rhs=2*mp.quad(lambda v:i1(delta(v)),[0,1])+z*mp.quad(lambda v:(1-2*v)**2*i2(delta(v)),[0,1])
  assert abs(rhs-2*i1(mass))<mp.mpf('1e-75') and abs(2*i1(mass))>mp.mpf('.1')
  ward_checks.append(mp.nstr(rhs-2*i1(mass),5))
 # Premature angular D=4 creates an epsilon times pole; cannot omit seagull.
 eps=s.Symbol('epsilon',positive=True);mass,z=s.symbols('M z',positive=True);Delta=mass+u*(1-u)*z
 pole=s.limit(eps*s.gamma(-1+eps)*Delta**(1-eps),eps,0,dir='+');assert pole==-Delta
 error=s.integrate(pole,(u,0,1));assert error==-mass-z/6
 # Actual noncommuting triple and parameter-gradient sign defect are separate
 # from the insensitive scalar two-point test.
 wit=json.loads((R/'calculations/canonical_so10_local_covariant_reference_witness/primary_result.json').read_bytes())
 ids=[i for i,n in enumerate(fields) if n.startswith('x_Phi_')];h,k,l,val=a['noncommuting_H_Phi_triple']
 phis=[]
 for hh in [h,k,l]:phis.append(mat(643,643,wit['actual12_homogeneous_carrier_matrices'][hh]).extract(ids,ids))
 triple=s.simplify((phis[2]*(phis[0]*phis[1]-phis[1]*phis[0])).trace());assert triple==s.sympify(val) and triple!=0
 assert 2*phis[0]!=s.zeros(54)
 # Lorentzian discontinuity of -log(Delta-i0) from its negative interval.
 rt=s.sqrt(s.Rational(1,2));interval=s.integrate((1-2*u)**2,(u,(1-rt)/2,(1+rt)/2))
 disc=2*s.pi*s.I*interval;assert s.simplify(disc-s.sympify(a['timelike_shape_discontinuity_at_8M']))==0 and disc!=0
 assert s.conjugate(disc)==-disc
 for folder,receipt in [('graded_causal_qap','validation_receipt_v2.json'),('causal_wick_bridge','validation_receipt.json'),
 ('causal_one_loop_sewing','validation_receipt.json'),('dimensional_stokes_primitive','validation_receipt.json'),
 ('local_covariant_reference_witness','validation_v2_receipt.json')]:
  assert json.loads((R/'calculations'/('canonical_so10_'+folder)/receipt).read_bytes())['execution_state']=='COMPLETED'
 performance={}
 for role in ['primary','replay']:
  cap=json.loads((O/(role+'_v2_capture.json')).read_bytes());res=json.loads((O/(role+'_v2_result.json')).read_bytes())
  assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and res['elapsed_after_imports']<120
  assert cap['launch']['memory']['available_pagefile']>=350*1024**2
  sample=max(v['private_bytes'] for v in cap['all_resource_samples']);assert sample<8*1024**3
  performance[role]={'seconds':res['elapsed_after_imports'],'max_sampled_private_bytes':sample}
 result={'schema':'BACKGROUND_REFERENCE_VALIDATION_V1','execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED',
  'scientific_disposition':'JOINT_FINITE_NORMALIZATION_TRANSPORT_AND_EXPLICIT_PERTURBATIVE_REFERENCE_MEMBER',
  'input_sha256':prep['input_sha256'],'performance':performance,'scalar_indices':a['scalar_indices'],
  'actual_H_Phi_gram':a['actual_H_scalar_grams']['Phi'],'nonzero_reference_shapes':shape_results,'series_terms':terms,
  'dimensional_ward_errors':ward_checks,'source_pairs':643,'background_affines':48,'BRST_color_matrices':45,
  'reference_and_source_derivatives_retained':True,'classical_switching_breaking_retained':True,
  'analytic_claims_use_named_qualified_domain_premises':True,'historical_old_calculations_freshly_replayed':False,
  'physical_reference_or_subtraction_scheme_adopted':False,'global_absolute_reference_phase_fixed':False,
  'full_E5_A5_or_all_loop_QAP_proved':False,'authority_changed':False,'native_failures':1,'verifier_failures':0,
  'shared_action_software_and_AI_author':True,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
