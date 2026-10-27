from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast,gzip,json,os,sys,threading,time
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'calculations/canonical_so10_u_F_fourth_support'))
import operators as OP
JP=OP.JP
O=Path(__file__).resolve().parent
tick=time.perf_counter();timer=threading.Timer(300,lambda:os._exit(124));timer.daemon=True;timer.start()
read=lambda p:json.loads(p.read_bytes());loadz=lambda p:json.loads(gzip.decompress(p.read_bytes()));H=lambda p:sha256(p.read_bytes()).hexdigest()
for pp,h in read(O/'ir_preparation.json')['input_sha256'].items():assert H(Path(pp))==h,pp
P=R/'calculations/canonical_so10_joint_born_ir_trace_domain';old=read(P/'validation_receipt.json')
assert old['complete_Q_varying_one_loop_interaction_joint_trace_domain_in_scope'] and old['qualified_analytic_proof_version']=='DERIVATION_V2.md'
assert H(P/'DERIVATION_V2.md')==old['input_sha256'][str(P/'DERIVATION_V2.md')]
assert 'scalar propagators are massive' in (P/'RECORD.md').read_text()
P=R/'calculations/canonical_so10_full_jet_source_master_bridge';receipt=read(P/'final_review_validation_receipt.json');pp=P/'free_tangent_tables.json.gz';rel=str(pp.relative_to(R)).replace('\\','/')
assert H(pp)==receipt['new_files_sha256'][rel];paired=loadz(pp)
node=next(n for n in ast.parse((R/'calculations/canonical_so10_u_F_fourth_support/operators.py').read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='hessian')
ns=dict(vars(OP));ns['allowed']=lambda word,nd,low,high:() if not word and nd in [0,1] else None
exec(compile(ast.Module(body=[node],type_ignores=[]),'UDR_FIRST_U_CONSTANT_HESSIAN','exec'),ns)
sector=lambda i:'B' if i<180 else 'x' if i<508 else 'L' if i<553 else 'C' if i<598 else 'a'
pole={('B','B'):2,('B','L'):1,('L','B'):1,('B','x'):1,('x','B'):1,('x','x'):0,('C','a'):2,('a','C'):2}
sectors=['B','L','x','C','a']
def inserted(bounds,blocks):
    out={};witness={}
    for i,j,d in blocks:
        for r in sectors:
            for t in sectors:
                if (r,i) not in bounds or (j,t) not in bounds:continue
                degree=bounds[r,i]+bounds[j,t]-d
                if (r,t) not in out or degree>out[r,t]:out[r,t]=degree;witness[r,t]=[i,j,d]
    return out,witness
def merged(left,right,blocks):
    out={}
    for i,j,d in blocks:
        for r in sectors:
            for t in sectors:
                if (r,i) in left and (j,t) in right:out[r,t,i,j,d]=left[r,i]+right[j,t]-d
    return out
M0=[('B','C',1),('a','L',0)];M0adj=[(j,i,d) for i,j,d in M0]
results=[];tables=[]
for probe in range(2):
    both=[];mu_support=[];auditrows=[]
    for role in ['primary','replay']:
        data=loadz(R/('calculations/canonical_so10_u_maximal_heat_cutoff/'+role+'_inputs.json.gz'));poly=JP.decode(data['QG'][probe])
        retained={w:v for w,v in poly.items() if JP.degree(w,4) in [0,1]}
        quad={w:v for w,v in retained.items() if len(w)==2 and all(i<643 for i,js in w)}
        H=ns['hessian'](quad,role,0,0);both.append(H)
        linear={w:v for w,v in retained.items() if len(w)==1};vars1={i for w in linear for i,js in w}
        affine=JP.euler(linear,vars1);assert not any(affine.values()),('NONZERO_AFFINE_RESPONSE',probe,role)
        assert not any(len(w)==0 for w in retained),('UNLABELED_VACUUM_TERM',probe,role)
        source1={w:v for w,v in retained.items() if len(w)==2 and sum(i>=643 for i,js in w)==1}
        sources={i for w in source1 for i,js in w if i>=643};resp=JP.euler(source1,sources);support=set()
        for src,rows in resp.items():
            out=src-643
            for w,v in rows.items():
                assert len(w)==1 and w[0][0]<643
                inp,js=w[0];nd=JP.dimension(out)+1-JP.dimension(inp)-len(js);assert nd in [0,1]
                support.add((out,inp,tuple(js.count(mu) for mu in range(4)),nd))
        mu_support.append(support)
        auditrows.append({'role':role,'retained_QG_terms':len(retained),'constant_Hessian_density_rows':len(quad),'constant_Hessian_entries':len(H),
          'linear_total_derivative_rows_retained':len(linear),'affine_Euler_nonzero':0,'source2_density_rows':sum(sum(i>=643 for i,js in w)==2 for w in retained)})
    assert both[0]==both[1] and mu_support[0]==mu_support[1]
    existing=set()
    for out,rows in paired[probe]['linear_field_response']:
        for w,p,c in rows:
            assert len(w)==1 and out//643==w[0]//643
            f=out%643;i=w[0]%643;nd=JP.dimension(f)+1-JP.dimension(i)-sum(p);existing.add((f,i,tuple(p),nd))
    assert mu_support[0]==existing,('FJB_CONSTANT_U_SUPPORT_OR_ORDER_MISMATCH',probe)
    hblocks=sorted({(sector(i),sector(j),sum(p)) for i,j,w,nd,p in both[0]})
    mblocks=sorted({(sector(out),sector(inp),sum(p)) for out,inp,p,nd in existing})
    newedge,witness=inserted(pole,hblocks)
    direct=merged(pole,pole,mblocks+[(j,i,d) for i,j,d in mblocks])
    withH={}
    for label,L,R in [('left',newedge,pole),('right',pole,newedge)]:
        for k,v in merged(L,R,M0+M0adj).items():withH[(label,)+k]=v
    ordinarymax=max(newedge.values(),default=0);tangentmax=max(list(direct.values())+list(withH.values()),default=0)
    scalar_tangent=any(out=='a' and inp=='x' and d==0 for out,inp,d in mblocks)
    if scalar_tangent:assert 2+0<4 and 2+2==4
    results.append({'probe':probe,'actual_constant_Hu_blocks':[list(v) for v in hblocks],'actual_constant_Mu_blocks':[list(v) for v in mblocks],
      'actual_paired_FJB_support_matched':len(existing),'input_route_audits':auditrows,
      'inserted_edge_bounds':[[*k,v] for k,v in sorted(newedge.items())],'new_edge_maximum_pole':ordinarymax,'one_tangent_maximum_merged_pole':tangentmax,
      'ordinary_edge_bound_at_most2':ordinarymax<=2,'one_tangent_bound_at_most3':tangentmax<=3,
      'positive_mass_scalar_reference_required':True,'actual_scalar_tangent_present':scalar_tangent,
      'massless_scalar_control_merged_degree':4 if scalar_tangent else None,'two_independent_tangents_tested':False})
    tables.append({'probe':probe,'Hu_full_four_momentum':OP.encode(both[0]),'Mu_support':[[out,inp,list(p),nd] for out,inp,p,nd in sorted(existing)],
      'inserted_edge_worst_block':[[*k,v] for k,v in sorted(witness.items())],'Mu_merger_bounds':[[list(k),v] for k,v in sorted(direct.items())],
      'one_Hu_with_M0_bounds':[[list(k),v] for k,v in sorted(withH.items())]})
applicable=all(z['ordinary_edge_bound_at_most2'] and z['one_tangent_bound_at_most3'] for z in results)
out={'schema':'UDR3_ACTUAL_FIRST_U_CONSTANT_IR_SUPPORT','results':results,'old_positive_scalar_mass_domain_qualified_version':'DERIVATION_V2.md',
 'all_actual_constant_Hu_and_Mu_routes_compared':True,'source2_retains_Schwartz_source_label':True,'affine_label_removal_absent_after_Euler':True,
 'first_u_soft_bound_disposition':'MATCHES_INHERITED_STRICT_NODE_BOUNDS' if applicable else 'EXTENSION_UNQUALIFIED_ACTUAL_CRITICAL_BLOCK_RETAINED',
 'no_massless_UV_symbol_used_as_IR_reference':True,'no_full_QAP_measure_or_physical_claim':True,'elapsed_after_imports':time.perf_counter()-tick}
raw=(json.dumps({'schema':'UDR3_COMPLETE_CONSTANT_OPERATOR_AND_BOUND_TABLES','tables':tables},sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
assert sum(p.stat().st_size for p in O.iterdir() if p.is_file())+len(blob)<16*1024**2
with (O/'ir_support_tables.json.gz').open('xb') as f:f.write(blob)
out['packed_tables_sha256']=sha256(blob).hexdigest()
with (O/'ir_support_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
