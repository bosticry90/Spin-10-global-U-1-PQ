"""GSK1 complete operator and support validation with independent probes."""
from data import *
def parse(v):return s.sympify(v,locals={'w':w})
def main():
    start=begin('validation_preparation.json',600)
    A=packed(HERE/'primary_tables.json.gz');Btab=packed(HERE/'replay_tables.json.gz')
    assert A['schema']==Btab['schema']=='GSK1' and A['domain_positions']==Btab['domain_positions']==30975
    assert A['basis']==Btab['basis'] and len(A['basis'])==177
    assert A['scalar_dimension']==Btab['scalar_dimension']==328 and A['classes']==Btab['classes']==35
    assert A['actual_Rh_O_intertwiners_checked']==Btab['actual_Rh_O_intertwiners_checked']==12
    for k in ['ghost_Casimir_operators','mass_sector_averaged_Casimir','scalar_Casimir_averages']:
        assert A[k]==Btab[k],k
    native=[]
    for role in ['primary','replay']:
        c=json.loads((HERE/f'{role}_capture.json').read_bytes());r=json.loads((HERE/f'{role}_result.json').read_bytes())
        assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
        blob=(HERE/f'{role}_tables.json.gz').read_bytes();assert sha256(blob).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['tables_sha256']
        assert r['elapsed_after_imports']<600 and c['launch']['memory']['available_pagefile']>=350*1024**2
        peak=max(v['private_bytes'] for v in c['all_resource_samples']);assert peak<=8*1024**3
        native.append({'role':role,'seconds':r['elapsed_after_imports'],'sampled_private_max':peak})
    ops={};floats=0;nonzero=0
    assert set(A['operators'])==set(Btab['operators'])=={f'{r},{t}' for r in range(5) for t in range(5)}
    for key in A['operators']:
        aa=[[parse(v) for v in row] for row in A['operators'][key]]
        bb=[[parse(v) for v in row] for row in Btab['operators'][key]]
        assert len(aa)==len(bb)==7 and all(len(row)==177 for row in aa+bb)
        for u,v in zip(aa,bb):
            for x0,y0 in zip(u,v):
                assert red(x0-y0)==0,(key,x0,y0);floats+=len(x0.atoms(s.Float));nonzero+=x0!=0
        ops[key]=aa
    assert floats==0
    values,fci,scm=inputs('primary');action,rho,V,ad,Ps,frame,Q,Qi,E=values;units=basis(frame)
    assert units==[tuple(v) for v in A['basis']]
    address={u:i for i,u in enumerate(units)};cs=[[parse(v) for v in row] for row in A['scalar_Casimir_averages']]
    C=list(map(dec,A['ghost_Casimir_operators']));average=[[parse(v) for v in row] for row in A['mass_sector_averaged_Casimir']]
    for r,P in enumerate(Ps):
        for i,M in enumerate(C):assert red(s.trace(P*M)-s.trace(P)*average[r][i])==0
    # Actual complete frame plus inherited SCM intertwiner certificate discharges
    # Schur completeness. Here check each retained Hermitian multiplicity block.
    small={};offdiag=0;rolechange=0;avgchanges=0
    for r in range(5):
        for t in range(5):
            key=f'{r},{t}';rev=f'{t},{r}';vv=ops[key];small[key]=[]
            for k in range(7):
                mats=[]
                for alpha,b in enumerate(frame['blocks']):
                    m=b['multiplicity'];M=s.SparseMatrix(m,m,{(i,j):vv[k][address[alpha,i,j]] for i in range(m) for j in range(m)})
                    zero(M-M.H);mats.append(M)
                    offdiag+=sum(i!=j and v!=0 for (i,j),v in M.todok().items())
                small[key].append(mats)
            for k in range(177):
                assert red(vv[0][k]-ops[rev][0][k])==0
                for i in range(3):
                    assert red(vv[1+i][k]-ops[rev][4+i][k])==0
                    avgchanges+=red(vv[1+i][k]-average[r][i]*vv[0][k])!=0
                    if r!=t:rolechange+=red(vv[1+i][k]-vv[4+i][k])!=0
            if r==0 or t==0:assert all(v==0 for row in vv for v in row)
    assert offdiag>0 and avgchanges>0 and rolechange>0
    assert avgchanges==sum(sum(v) for v in A['averaged_Casimir_change_positions'].values())
    dualchanges=0
    for key,row in Btab['wrong_dual_raw'].items():
        dualchanges+=sum(red(parse(v)-u)!=0 for u,v in zip(ops[key][0],row))
    assert dualchanges>0
    types=small_types(fci);counts=[red(sum(b['dimension']*s.trace(P) for b,P in zip(frame['blocks'],row))) for row in types]
    assert counts==[290,5,8,1,12,12]
    O=dec(action['vacuum']['orbit'])
    for which in [0,1]:
        F=tidy(Q*inflate(frame['blocks'],types[which])*Qi);zero(F-F.T);zero(F*F-F);zero(O.T*F)
    # These zeros imply projected T is symmetric only on physical/soft carriers
    # using T_ab-T_ba=f_ab^c O_c. Do not extend this inference to Goldstones.
    P0=packed(CAL/'canonical_so10_ghost_scalar_support/primary_support_tables.json.gz')
    gnorm={(n['antighost'],n['ghost'],n['scalar_type']):parse(n['norm_squared']) for n in P0['norms']}
    pp={(p['first_ghost'],p['second_ghost'],p['scalar_type']):p for p in A['probes']}
    rp={(p['first_ghost'],p['second_ghost'],p['scalar_type']):p for p in Btab['probes']}
    assert len(pp)==len(rp)==150
    rawprofiles=[];charged=[];excluded=[];goldbad=0;goldnegative=0;Hdiagchanges=0
    # Matrix-trace probes differ from the workers' vectorized pairing helper.
    for r in range(5):
        for t in range(5):
            key=f'{r},{t}';mats=small[key]
            for typ,Ps0 in enumerate(types):
                qraw=[red(sum((b['dimension']*s.trace(M*P) for b,M,P in zip(frame['blocks'],row,Ps0)),s.S.Zero)) for row in mats]
                scalar=[red(sum((b['dimension']*cs[a][i]*s.trace(M*P) for a,(b,M,P) in enumerate(zip(frame['blocks'],mats[0],Ps0))),s.S.Zero)) for i in range(3)]
                probe=pp[r,t,typ];replay=rp[r,t,typ]
                expected=[parse(probe['raw']),*map(parse,probe['q1_squared']),*map(parse,probe['q2_squared'])]
                expected2=[parse(replay['raw']),*map(parse,replay['q1_squared']),*map(parse,replay['q2_squared'])]
                assert all(red(a-b)==0 for a,b in zip(qraw,expected)) and all(red(a-b)==0 for a,b in zip(qraw,expected2))
                assert all(red(a-parse(b))==0 for a,b in zip(scalar,probe['qscalar_squared']))
                assert all(red(a-parse(b))==0 for a,b in zip(scalar,replay['qscalar_squared']))
                if typ in [0,1]:assert red(qraw[0]-gnorm[r,t,typ])==0
                if qraw[0]!=0:rawprofiles.append([r,t,typ])
                if any(v!=0 for v in qraw[1:]+scalar):charged.append([r,t,typ])
                if gnorm[r,t,typ]==0 or gnorm[t,r,typ]==0:
                    assert all(v==0 for v in qraw+scalar);excluded.append([r,t,typ])
                if typ>=2:
                    goldbad+=red(qraw[0]-gnorm[r,t,typ])!=0
                    if qraw[0].is_negative:goldnegative+=1
            Hs=[dec(b['H']) for b in fci['blocks']]
            diag=[s.diag(*H.diagonal()) for H in Hs]
            for row in mats:
                change=red(sum((b['dimension']*s.trace(M*(H-HD)) for b,M,H,HD in zip(frame['blocks'],row,Hs,diag)),s.S.Zero))
                Hdiagchanges+=change!=0
    assert len(excluded)==128 and goldbad>0
    softprofiles=[v for v in rawprofiles if v[2]==1];assert softprofiles==[[1,4,1],[4,1,1]]
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<6*1024**2
    out={'schema':'GSK1_VALIDATION','execution_state':'COMPLETED','status':'QUALIFIED_COMPLETE_ORDERED_GHOST_SCALAR_CHARGE_OPERATORS',
      'scalar_dimension':328,'classes':35,'commutant_units':177,'ghost_pairs':25,'operators_per_pair':7,
      'complete_operator_positions':30975,'nonzero_operator_positions':nonzero,'zero_operator_positions':30975-nonzero,
      'light_pair_operator_positions':9*7*177,'exact_native_operator_equality':True,'actual_intertwiners':12,
      'closed_type_probe_positions':150,'raw_nonzero_profiles':rawprofiles,'F2_nonzero_profiles':charged,
      'raw_profile_count':len(rawprofiles),'F2_profile_count':len(charged),'structurally_excluded_profiles':len(excluded),
      'scalar_soft_profiles':softprofiles,'physical_soft_raw_norm_equalities':50,
      'ghost_Casimir_averaging_change_positions':avgchanges,'wrong_scalar_dual_change_positions':dualchanges,
      'mass_role_exchange_change_positions':rolechange,'off_diagonal_operator_positions':offdiag,
      'Gold_Frobenius_replacement_change_profiles':goldbad,'negative_Gold_raw_profiles':goldnegative,
      'diagonal_H_trace_change_operator_count':Hdiagchanges,'exact_UV_arithmetic_no_float_atoms':True,
      'SCM_actual_commutator_and_frame_certificate':'REUSED_AUTHENTICATED_NOT_RERUN','native_runs':native,
      'full_model_ghostS_amplitude_calculated':False,'full_C1_or_E5_qualified':False,
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'shared_limits':['action','reference','scalar frame','exact ring/software','AI authorship'],
      'elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'validation_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'status':out['status'],'elapsed_after_imports':out['elapsed_after_imports'],
      'receipt_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
if __name__=='__main__':main()
