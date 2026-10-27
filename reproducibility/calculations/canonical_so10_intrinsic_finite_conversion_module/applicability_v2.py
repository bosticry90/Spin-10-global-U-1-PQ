from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));H=lambda p:sha256(p.read_bytes()).hexdigest();tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'applicability_preparation_v2.json')['input_sha256'].items():assert H(Path(p))==h,p
d=load(O.parent/'canonical_so10_intrinsic_ghost_hatted/primary_inputs.json.gz');audit=d['audit'];names=audit['names'];geo=audit['geometry'];base=geo['names'];fields={names.index(base[i]) for i,J,h,k in geo['field_source_h_k']};sources={names.index(base[J]):base[i] for i,J,h,k in geo['field_source_h_k']};summary=[]
for name in ['physical_G','physical_QG']:
 for probe,p in enumerate(audit[name]):
  rows=0;firstsource=0;scalar_sources=0;source0_terms=0;first_flow_survivors=0;conjugates=set()
  for gp,word,ci in p['monomials']:
   src=[(nn,I) for nn,I in word if nn in sources];rows+=1;scalar_sources+=sum(sources[nn].startswith('x_') for nn,I in src);source0_terms+=not src;firstsource+=len(src)==1
   for nn,I in src:conjugates.add(sources[nn])
   vanish=sum(not(nn in fields and names[nn].startswith('C')) for nn,I in word)
   # Jx is absent, so every non-C factor vanishes on the stated ideal.
   # Two such factors suffice: every first derivative still leaves one.
   if vanish<2:first_flow_survivors+=1
  assert scalar_sources==first_flow_survivors==0
  assert all(z.startswith(('bar','ub','b','L')) for z in conjugates)
  summary.append({'operation':name,'probe':probe,'density_positions':rows,'source_degree1_rows':firstsource,'source_Jx_rows':scalar_sources,'source0_rows_retained':source0_terms,'first_derivative_surviving_on_C_Jx_ideal':first_flow_survivors,'conjugate_field_names':sorted(conjugates)})
assert sum(z['density_positions'] for z in summary)==105661
hat=d['hat_vertices'];assert len(hat)==3;ports=[]
for row in hat:
 ww=[p for p,j in row['ports']];assert len(ww)==3 and set(ww)<=set(['P','S','c']);assert ww.count('c')==1 and sum(z in ['P','S'] for z in ww)==2;ports.append(ww)
source=load(O/'primary_inputs.json.gz');assert all(len(row['word'])==2 and sum(z.startswith('C') for z in row['word'])==1 and sum(z.startswith('x_') for z in row['word'])==1 for rows in source['source_Qx'].values() for row in rows)
v=read(O/'validation_receipt.json');m=read(O/'mass_receipt.json');assert m['residual_positions']==0 and v['component_cochain_and_odd_Leibniz_routes_agree'];counts=v['results'][1]['prime_logs'];assert all(counts[p]['H']==320 and counts[p]['F']==2452 and counts[p]['dF']==0 for p in ['2','3'])
out={'schema':'IFC3_SOURCE_ROOT_STRUCTURAL_APPLICABILITY_V2','elapsed_after_imports':time.perf_counter()-tick,'actual_full_G_QG_source_audit':summary,'actual_Ihat_port_families':ports,'Ihat_one_loop_connected_Jx_support':'EMPTY_FERMION_COMPONENT_CANNOT_REACH_SOURCE','source_tangent_trace_Jx':'ZERO_SOURCE_INDEPENDENT_FIELD_MAPS','source_root_status':'DETERMINED_BY_QUALIFIED_CSW_ONE_VARIATION_IDENTITY_NOT_DIRECT_INDEPENDENT_REPLAY','rho_Jx_C_heat_root':'MINUS_H','u_Jx_CC_heat_root':'MINUS_F','source_derivatives_before_restriction':True,'inherited_common_trace_and_relative_UV_jet_premises_required':True,'full_restoration_normalization_QAP_E5_A5_authority':False};print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
