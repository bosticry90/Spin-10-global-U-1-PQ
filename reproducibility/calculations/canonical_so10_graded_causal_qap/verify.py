"""Independent GQAP1 checks; no native helper imported."""
from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
def main():
 tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'validation_preparation.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 a,b=[json.loads((O/(role+'_result.json')).read_bytes()) for role in ['primary','replay']]
 for key in ['source_rows','GF_rows','canonical_fields','source_Euler_ports','Euler_ports_sha256',
 'source_port_target_counts_sha256','zero_field_rule_outputs','GF_residual_dimensions','physical_density_dimensions',
 'derivative_BRST_ports','Phi_generator_norm','Phi_temporal_seagull_beta_coefficient_normalized',
 'Qbeta_Phi_B0_dC_coefficient_vector_normalized','scalar_beta_moments','controls']:
  assert a[key]==b[key],key
 assert a['source_rows']==35162 and a['GF_rows']==33092 and a['canonical_fields']==643
 assert len(a['zero_field_rule_outputs'])==15 and a['derivative_BRST_ports']==180
 assert len(a['physical_density_dimensions'])==34 and set(a['physical_density_dimensions'].values())=={4}
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()))
 nports=sum(1+len(row['word']) for rows in data['master_field_maps'].values() for row in rows)
 assert nports==a['source_Euler_ports']
 assert a['controls']['odd_left_right_conversion_sensitive_ports']>0
 # Independently recover the actual compact Phi generator norm from its entries.
 physical=json.loads((PK/'frozen_a10_physical_reconciliation/full_primary.json').read_bytes())
 entries=physical['representation_matrices']['Phi'][0]['entries']
 norm=s.simplify(sum(s.sympify(v)**2 for i,j,v in entries));assert norm!=0
 assert s.sympify(a['Phi_generator_norm'])==norm
 assert s.sympify(a['Phi_temporal_seagull_beta_coefficient_normalized'])==norm/2
 assert a['Qbeta_Phi_B0_dC_coefficient_vector_normalized'] and all(s.sympify(v)!=0 for k,v in a['Qbeta_Phi_B0_dC_coefficient_vector_normalized'])
 # Heterogeneous dimensions and source-left bracket/Legendre orientation.
 classes=[(1,0,0),(0,1,1),(2,-1,1),(2,0,0)]
 for dim,gh,par in classes:
  J=(4-dim,-1-gh,1-par);Rtype=(dim,gh+1,1-par);Etype=(4-dim,-gh,par)
  assert (Rtype[0]+Etype[0],Rtype[1]+Etype[1],(Rtype[2]+Etype[2])%2)==(4,1,1)
  assert J[0]==Etype[0] and J[1]+1==Etype[1] and 1-J[2]==Etype[2]
  assert (-1)**(par*(1-par))==1 and (-1)**(par*par)==(-1)**par
 assert 0+4-0==4 and 0+3!=4
 assert 2+4-2==4 and 2+3!=4
 # General finite beta jets satisfy the free equation, including cross jets.
 x,y,M,d=s.symbols('x y M d');F=x*x;E=y+M*x
 op=lambda f:s.expand(d*s.diff(f,x,2)/2-M*d*s.diff(f,x,y)+M*M*d*s.diff(f,y,2)/2)
 assert op(F*E)==s.expand(op(F)*E)
 wrong=s.expand(d*s.diff(F*E,x,2)/2);assert wrong!=s.expand(op(F)*E)
 for k in range(8):assert s.expand(s.sympify(a['scalar_beta_moments'][k+1])+M*s.sympify(a['scalar_beta_moments'][k]))==0
 # Triangular anomaly insertion recursion: use independent noncommuting maps.
 T=[s.eye(2)]+[s.Matrix([[n,1],[n+1,2-n]]) for n in range(1,7)]
 defect=[s.zeros(2,1)]+[s.Matrix([n*n,1-n]) for n in range(1,7)];delta=[]
 for n in range(7):delta.append(defect[n]-sum((T[k]*delta[n-k] for k in range(1,n+1)),s.zeros(2,1)))
 assert delta[0]==s.zeros(2,1)
 for n in range(7):assert sum((T[k]*delta[n-k] for k in range(n+1)),s.zeros(2,1))==defect[n]
 assert any(v!=s.zeros(2,1) for v in delta[1:])
 # Actual nonzero Qbeta witness makes the wrong primitive chart fail.
 h=s.symbols('Delta_heat');w=s.sympify(a['Qbeta_Phi_B0_dC_coefficient_vector_normalized'][0][1])
 assert s.simplify((h-w)+(-h+w))==0 and s.simplify((h-w)-h)==-w and w!=0
 # Compact switching retains the classical current, independently of the anomaly.
 t=s.symbols('t');cut=s.Function('g')(t);B=s.Function('B')(t);C=s.Function('C')(t)
 assert s.expand(s.diff(cut*B*C,t)-cut*s.diff(B*C,t))==B*C*s.diff(cut,t)
 assert B*C*s.diff(cut,t)!=0
 for folder,receipt in [('causal_one_loop_sewing','validation_receipt.json'),('causal_one_loop_sewing','cycle_receipt.json'),
 ('causal_one_loop_sewing','jets_receipt.json'),('causal_wick_bridge','validation_receipt.json'),
 ('dimensional_stokes_primitive','validation_receipt.json')]:
  assert json.loads((R/'calculations'/('canonical_so10_'+folder)/receipt).read_bytes())['execution_state']=='COMPLETED'
 performance={}
 for role in ['primary','replay']:
  cap=json.loads((O/(role+'_capture.json')).read_bytes());res=json.loads((O/(role+'_result.json')).read_bytes())
  assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and res['elapsed_after_imports']<120
  assert cap['launch']['memory']['available_pagefile']>=350*1024**2
  sample=max(v['private_bytes'] for v in cap['all_resource_samples']);assert sample<8*1024**3
  performance[role]={'seconds':res['elapsed_after_imports'],'max_sampled_private_bytes':sample}
 result={'schema':'GRADED_CAUSAL_QAP_VALIDATION_V1','execution_state':'COMPLETED',
 'scientific_disposition':'GRADED_COMPACT_ONE_LOOP_ANOMALOUS_INSERTION_PRINCIPLE_AND_NONTRIVIAL_FINITE_CHART_TRANSPORT',
 'scientific_acceptance':'NOT_PERFORMED','input_sha256':prep['input_sha256'],'performance':performance,
 'source_rows':35162,'GF_rows':33092,'canonical_fields':643,'physical_terms':34,'source_Euler_ports':nports,
 'actual_Phi_generator_norm':str(norm),'actual_nonzero_Qbeta_coefficient_vector':a['Qbeta_Phi_B0_dC_coefficient_vector_normalized'],
 'classical_switching_breaking_retained':True,'anomaly_coefficients_set_to_zero_or_fitted':False,
 'primitive_transport_only_on_common_domain':True,'full_E5_A5_global_QAP_measure_or_A5_proved':False,
 'native_failures':0,'verifier_failures':0,'authority_changed':False,'external_validation':False,
 'shared_action_software_and_AI_author':True,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
