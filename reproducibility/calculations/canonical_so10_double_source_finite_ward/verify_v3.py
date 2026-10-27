from data_v3 import *
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation_v3.json')['input_sha256'].items():assert digest(Path(p))==h,p
P=packed(HERE/'primary_v2_tables.json.gz');R=packed(HERE/'replay_v3_tables.json.gz')
for k in ['source_columns','qC_columns','pieces','total','image']:assert P[k]==R[k],k
for k in ['A','source_dual','Cinv','Cphys']:zero(dec(P['charts'][k])-dec(R['charts'][k]))
assert not R['new_measured_parent_or_primary_image_read']
parent=get_parent();E={tag:list(map(fromrows,ps)) for tag,ps in P['source_columns'].items()};QC=list(map(fromrows,P['qC_columns']));pieces={tag:fromrows(ps) for tag,ps in P['pieces'].items()};total=fromrows(P['total']);assert add(*pieces.values())==total and len(parent)==5470
S={i:{(a,b):co(z) for a,b,z in rs} for i,rs in read(CAL/'canonical_so10_double_auxiliary_source_pole/actual_primary_v2_result.json')['actual_tensors']['S']}
for l in range(45):
 expected={}
 for i,mat in S.items():
  for (ll,h),v in mat.items():
   if ll==l:
    w,ph=mulword(((f'JLp{i}',()),),((f'Cp{h}',()),));addto(expected,w,ph*g*v)
 assert clean(expected)==E['source_JL'][l]
 assert E['source_Ja'][l]==scale(var(f'JAp{l}'),-1)
# Complete source-pair differentiated Ward identity, including both W legs.
by_pair={}
for w,z in parent.items():
 i,j=int(w[0][0][3:]),int(w[1][0][3:]);by_pair.setdefault((i,j),{})[w[2:]]=z
def pp(i,j):return by_pair.get((i,j),{}) if i<j else scale(by_pair.get((j,i),{}),-1) if j<i else {}
def qc(p):
 out={}
 for w,z in p.items():
  for k,(n,j) in enumerate(w):
   assert n.startswith('Cp') and not j
   for image,v in QC[int(n[2:])].items():
    word,ph=mulword(w[:k],image,w[k+1:])
    if ph:addto(out,word,z*v*ph*(-1)**k)
 return clean(out)
high=add(pieces['source_JL'],pieces['qC']);highpairs=defaultdict(dict)
for w,z in high.items():
 assert [typ(n) for n,j in w]==['JL','JL','C','C','C'] and not any(j for n,j in w)
 highpairs[int(w[0][0][3:]),int(w[1][0][3:])][w[2:]]=z
comm={};bare={};full_rhs={}
for i,j in itertools.combinations(range(45),2):
 qpart=qc(pp(i,j));ws={}
 for (l,h),v in S.get(i,{}).items():
  for w,z in product(var(f'Cp{h}'),pp(j,l)).items():addto(ws,w,g*v*z)
 for (l,h),v in S.get(j,{}).items():
  for w,z in product(var(f'Cp{h}'),pp(i,l)).items():addto(ws,w,-g*v*z)
 ws=clean(ws);rhs=add(qpart,ws);assert rhs==highpairs.get((i,j),{}),(i,j)
 if ws:comm[i,j]=ws
 if qpart:bare[i,j]=qpart
 if rhs:full_rhs[i,j]=rhs
ja=pieces['source_Ja'];assert len(ja)==2*len(parent)
for w in ja:assert [typ(n) for n,j in w]==['Ja','JL','C','C'] and not any(j for n,j in w)
derivative_commutator_omission=sum(len(p) for p in comm.values())
counts={tag:len(p) for tag,p in pieces.items()};types=Counter()
dims={'B':1,'X':1,'A':1,'L':2,'C':1,'a':1,'Ja':2,'JL':1};ghost={'B':0,'X':0,'A':0,'L':0,'C':1,'a':-1,'Ja':0,'JL':-1}
for tag,p in pieces.items():
 for w,z in p.items():
  kinds=[typ(n) for n,j in w];typed_dim=sum(dims[k] for k in kinds)+sum(len(j) for n,j in w)+(1 if tag=='GF_Xv' else 0)
  assert typed_dim==5 and sum(ghost[k] for k in kinds)==1 and sum(odd(n) for n,j in w)%2==1
  assert co(s.conjugate(z).subs({s.conjugate(g):g,s.conjugate(xi):xi,s.conjugate(eta):eta})-z)==0
  types[','.join(sorted(kinds))+';jets'+str(sum(len(j) for n,j in w))+';v'+str(int(tag=='GF_Xv'))]+=1
source2=add(ja,high);source1=add(*(pieces[tag] for tag in GROUPS if tag.startswith('GF_')))
assert add(source1,source2)==total and ja and P['controls']['wrong_even_replacement_changed_positions']>0
Jnames=sorted({n for w in ja for n,j in w if n.startswith('JAp')});witness_name=Jnames[0];witness=EL(total,witness_name);assert witness and not any(j for w in witness for n,j in w)
out={'status':'QUALIFIED_FULL_ACTUAL_FINITE_CONTACT_WARD_IMAGE_AND_TWO_SOURCE_DERIVATIVE_RELATION','elapsed_after_imports':time.perf_counter()-t,'parent_nonzero':len(parent),'full_Ward_image_nonzero':len(total),'piece_counts':counts,'source_degree2_nonzero':len(source2),'source_degree1_parent_contribution_nonzero':len(source1),'JLJLCCC_combined_nonzero':len(high),'JaJLCC_nonzero':len(ja),'all990_two_JL_derivative_pairs_checked':True,'two_source_Ward_rhs_nonzero':sum(len(p) for p in full_rhs.values()),'bare_twice_source_kernel_qC_nonzero':sum(len(p) for p in bare.values()),'commutator_companion_nonzero':derivative_commutator_omission,'omitted_W_companions_sensitive':derivative_commutator_omission>0,'highest_source_JaJLCC_domain':45*45*990,'highest_source_JLJLCCC_domain':990*14190,'Euler_Ja_witness':witness_name,'witness_nonzero':len(witness),'source_Euler_columns_checked':45,'source_linear_connection_matches_actual_S':True,'source_Ja_Lorentz_sign':-1,'source_Ja_Euclidean_sign':'I','source_degree_filtration':'b preserves or lowers source degree; no source>=3 local parent; highest-source relative image complete','coefficient_factor':'g10^4*log(2)/(16pi^2) multiplying the displayed Lorentzian image; restore the SAME Wick/source pullback','controls':P['controls'],'image_type_counts':dict(types),'relative_quantum_Ward_comparison_qualified_in_matched_single_variation_scope':True,'absolute_Slavnov_breaking_or_restoration_qualified':False,'arbitrary_two_Q_or_coincident_products_QAP_measure_phase_E5A5_qualified':False,'physical_scheme_adopted':False,'authority':'34/39','scientific_acceptance':'NOT_PERFORMED'}
out.update({'GF_scalar_scope':'FROZEN_v0_ONLY; generic w requires separate extension','generic_z_GF_source_degree1_qualified':False,'highest_source_JaJaC_zero_slots':46575,'highest_source_domain_with_JaJaC':16099425})
raw=(json.dumps({'scope':out,'complete_native_images':{'primary':{'path':str(HERE/'primary_v2_tables.json.gz'),'packed_sha256':digest(HERE/'primary_v2_tables.json.gz'),'full_Ward_image_key':'total','complete_pieces_key':'pieces'},'replay':{'path':str(HERE/'replay_v3_tables.json.gz'),'packed_sha256':digest(HERE/'replay_v3_tables.json.gz'),'full_Ward_image_key':'total','complete_pieces_key':'pieces'}},'source_degree2_image_definition':'sum pieces[source_Ja,source_JL,qC]','source_degree1_parent_definition':'sum all GF_* pieces','two_source_commutator_definition':'D_j D_i of complete primary pieces[source_JL]; checked for every i<j against W_i D_jP-W_j D_iP','Euler_Ja_witness':serial(witness),'evidence_not_truncated':True},sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'selected_contact_Ward_descendants_v3.json.gz').open('xb') as f:f.write(blob)
out.update({'artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest()});print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
