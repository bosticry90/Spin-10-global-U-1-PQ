"""G2P1 complete source algebra and common-scale nine-family inputs."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
J,L,lg,z,zz=s.symbols('J L lg z zeta2',real=True);hs=s.symbols('h1:5',real=True);d=s.Symbol('d',positive=True);ep=s.Symbol('eps',real=True)
LOC={str(v):v for v in [J,L,lg,z,zz,d,ep,*hs]};lams=[s.Rational(3,10),s.Rational(3,2),s.Integer(25),s.Rational(253,10)];ks=[d]+[v/60 for v in lams]
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def receipt(folder,file='validation_receipt.json'):return json.loads((CAL/folder/file).read_bytes())
def expr(v):return s.sympify(v,locals=LOC)
def clean(v):
    v=s.expand_log(s.expand(v),force=False);replacements={}
    for atom in v.atoms(s.log):
        a=atom.args[0]
        if a.is_Rational and a>0:
            replacements[atom]=sum(n*s.log(p) for p,n in s.factorint(int(a.p)).items())-sum(n*s.log(p) for p,n in s.factorint(int(a.q)).items())
    return s.cancel(s.expand(v.xreplace(replacements)))
def common(v):
    return clean(expr(v).subs({z:J-s.log(60),**{h:s.log(m/60) for h,m in zip(hs,lams)},zz:s.zeta(2)}))
def begin(prep='preparation.json'):
    start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),
      'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def mat(raw):return s.SparseMatrix(*raw['shape'],{(i,j):s.sympify(v) for i,j,v in raw['entries']})
def q(v):
    a,sep,b=str(v).partition('/');return mp.mpf(a)/mp.mpf(b) if sep else mp.mpf(a)
def number(v):return mp.mpf(str(s.N(clean(v),95)))
def fmt(v):return mp.nstr(v,45)
def vec(v):return list(map(str,v))

def quartic(role):
    qir=packed(CAL/'canonical_so10_vector_quartic_ir_matching'/f'{role}_tables.json.gz');qus=packed(CAL/'canonical_so10_vector_quartic_uv_subgraphs'/f'{role}_tables.json.gz')
    primitive=packed(CAL/'canonical_so10_vector_quartic_primitive'/f'{role}_v2_tables.json.gz');out=[]
    for h in range(3):
        if role=='primary':
            # Take the pole from all original internal sectors first. Color
            # contractions are from the actual opened matrices, not the target.
            P=list(map(mat,packed(CAL/'canonical_so10_width_hard_projection/primary_tables.json.gz')['projectors']))
            bft=packed(CAL/'canonical_so10_background_threshold_inputs/primary_tables.json.gz');V=mat(qir['light_embedding']);adj=[s.SparseMatrix(45,45,{}) for _ in range(45)]
            for a,b,c,v in bft['f']:adj[a][c,b]=s.sympify(v)
            T=sum((V[a,[0,1,4][h]]*adj[a] for a in range(45)),s.zeros(45));mass=list(map(mat,qir['mass_operators']));curv=list(map(mat,qir['first_curvature_operators'][h]));ct={-2:0,-1:0,0:0}
            for r in range(1,5):
                A=clean(s.trace(P[r]*T*T*sum((ks[t]*mass[t] for t in range(5)),s.zeros(45)))/ks[r]);B=clean(-s.trace(P[r]*T*sum(curv,s.zeros(45))));jr=z-hs[r-1]
                E=1+ep*jr+ep**2*(jr**2+zz)/2
                expansion=s.expand(((30+3*ep)*A/ep+24*B/ep**2)*E)
                for power in ct:ct[power]+=expansion.coeff(ep,power)
            bare={p:expr(qir['polynomials'][h]['hard_bare_remainder'][str(p)]) for p in ct};pol={p:common((bare[p]+ct[p]).subs(d,0)) for p in ct}
            ct_common={p:common(v.subs(d,0)) for p,v in ct.items()}
        else:
            pol={p:common(qus['insertions'][h]['bare_plus_CT_full_DIAGNOSTIC'][str(p)]) for p in [-2,-1,0]}
            ct_common={p:common(expr(qus['insertions'][h]['CT_full_positive_d'][str(p)]).subs(d,0)) for p in [-2,-1,0]}
        # Independently generated restricted-tree EFT quartic and its two cuts.
        X=expr(qir['EFT_color'][h]['X']);Z=expr(qir['EFT_color'][h]['Z']);j0=s.Symbol('j0',real=True)
        E=1+ep*j0+ep**2*(j0*j0+zz)/2;kap=30-17*ep-2*ep**2
        ef=s.series(-kap*X*E**2/(ep*(1-ep))-12*Z*E**2/ep**2+((30+3*ep)*X/ep+24*Z/ep**2)*E,ep,0,1).removeO().expand()
        eft={p:clean(ef.coeff(ep,p)) for p in [-2,-1]};assert all(not v.has(j0) for v in eft.values())
        # Old light-only insertion is a separately measured omitted-part control.
        light={p:common(qus['insertions'][h]['CT_light_limit'][str(p)]) for p in [-2,-1,0]}
        out.append({'family':{str(p):str(clean(v)) for p,v in pol.items()},'EFT':{str(p):str(v) for p,v in eft.items()},'omitted_light_insertion':{str(p):str(v) for p,v in light.items()},
          'CT_heavy_projection':{str(p):str(v) for p,v in ct_common.items()},
          'original_CT_full_positive_d':qus['insertions'][h]['CT_full_positive_d'],'original_CT_light_positive_d':qus['insertions'][h]['CT_light_positive_d']})
    return out

def source_data(role):
    v3=packed(CAL/'canonical_so10_three_vector_sunset'/('primary_v2_tables.json.gz' if role=='primary' else 'replay_v2_tables.json.gz'))
    gv=packed(CAL/'canonical_so10_ghost_vector_sunset'/('primary_v2_tables.json.gz' if role=='primary' else 'replay_tables.json.gz'))
    vss=packed(CAL/'canonical_so10_scalar_current_vss_assembly/primary_assembly_tables.json.gz');vr=receipt('canonical_so10_scalar_current_vss_assembly')
    vvs=receipt('canonical_so10_vector_vector_scalar_sunset');gs=receipt('canonical_so10_ghost_scalar_sunset');vs=packed(CAL/'canonical_so10_vector_scalar_quartic'/f'{role}_amplitude_tables.json.gz')
    s4=packed(CAL/'canonical_so10_scalar_quartic_amplitude'/f'{role}_tables.json.gz');s3=packed(CAL/'canonical_so10_scalar_cubic_amplitude'/f'{role}_tables.json.gz')
    return v3,gv,vss,vr,vvs,gs,vs,s4,s3

def assemble(role):
    Q=quartic(role);v3,gv,vss,vr,vvs,gs,vs,s4,s3=source_data(role)
    poles={name:{'-2':['0']*3,'-1':['0']*3} for name in ['VVVV','VVSS','VSS','ghostS','VVS','ghostV','VVV','SSSS','SSS']}
    poles['VVVV']={str(p):[v['family'][str(p)] for v in Q] for p in [-2,-1]}
    poles['VVV']={'-2':v3['pole2'],'-1':[str(clean(expr(a)+expr(b)*J)) for a,b in zip(v3['pole1'],v3['pole1_J'])]}
    poles['ghostV']['-1']=gv['remaining_pole'];poles['VVS']['-1']=vvs['remaining_overall_poles'];poles['VSS']['-1']=[v[0] for v in vss['cases']['0.5']['coefficients']]
    # Explicit zero evidence from completed family kernels, not absent entries.
    assert gs['overall_poles']==['0']*3 and s4['remaining_overall_pole']==s3['remaining_overall_pole']==[0]*3
    for i in range(3):
        assert expr(vs['kernels']['bareU'][0])+expr(vs['kernels']['ctU'][0])==0
        assert expr(vs['kernels']['bareW'][0])+expr(vs['kernels']['ctW'][0])==0
    eft={name:{'-2':['0']*3,'-1':['0']*3} for name in poles}
    eft['VVVV']={str(p):[v['EFT'][str(p)] for v in Q] for p in [-2,-1]}
    eft['VVV']={'-2':v3['all_light_EFT_pole2'],'-1':v3['all_light_EFT_pole1']};eft['ghostV']['-1']=gv['all_light_EFT_pole'];eft['VSS']['-1']=vr['common_EFT_poles']
    total={str(p):[clean(sum(expr(v[str(p)][i]) for v in poles.values())) for i in range(3)] for p in [-2,-1]}
    light={str(p):[clean(sum(expr(v[str(p)][i]) for v in eft.values())) for i in range(3)] for p in [-2,-1]}
    parent={str(p):[clean(a+b) for a,b in zip(total[str(p)],light[str(p)])] for p in [-2,-1]}
    quadratic=[clean(expr(v['family']['0']).coeff(J,2)+expr(v3['scale_J2'][i])) for i,v in enumerate(Q)]
    return Q,(v3,gv,vss,vr,vvs,gs,vs,s4,s3),{'families':poles,'EFT_families':eft,'heavy_sum':{p:vec(v) for p,v in total.items()},'EFT_sum':{p:vec(v) for p,v in light.items()},'parent_sum':{p:vec(v) for p,v in parent.items()},'finite_L_squared_coefficient_inside_g2':vec(quadratic)}

def finite_cases(role,Q,src):
    v3,gv,vss,vr,vvs,gs,vs,s4,s3=src;out={}
    for gskey in ['1/2','1']:
        g2=q(gskey);case='0.5' if gskey=='1/2' else '1.0';j=mp.log(60)-mp.log(g2)
        values={name:[[mp.mpf(0)]*3 for h in range(3)] for name in ['VVVV','VVSS','VSS','ghostS','VVS','ghostV','VVV','SSSS','SSS']}
        for h in range(3):
            poly=expr(Q[h]['family']['0']);values['VVVV'][h]=[g2*number(poly.subs(J,s.Float(mp.nstr(j,110),110))),g2*number(s.diff(poly,J).subs(J,s.Float(mp.nstr(j,110),110))),g2*number(poly.expand().coeff(J,2))]
            a,b,c=q(v3['finite_F0'][h]),number(expr(v3['scale_J'][h])),number(expr(v3['scale_J2'][h]));values['VVV'][h]=[g2*(a+b*j+c*j*j),g2*(b+2*c*j),g2*c]
            a,b=q(gv['finite_F0'][h]),number(expr(gv['scale_J'][h]));values['ghostV'][h]=[g2*(a+b*j),g2*b,mp.mpf(0)]
            line=vss['cases'][case]['coefficients'][h] if role=='primary' else next(r for r in vr['common_scale_cases'] if r['g2']==case)['coefficients'][h]
            values['VSS'][h]=[g2*q(line[1]),g2*q(line[2]),mp.mpf(0)]
            for name,data in [('VVS',vvs),('ghostS',gs)]:
                line=data['cases'][case];values[name][h]=[g2*q(line['finite_L0'][h]),g2*q(line['L_coefficient'][h]),mp.mpf(0)]
            for name,data in [('SSSS',s4),('SSS',s3)]:
                line=data['cases'][gskey];values[name][h]=[q(line['finite_L0'][h]),q(line['scale_linear'][h]),mp.mpf(0)]
            for power in vs['coupling_powers']:
                line=vs['coefficients'][str(power)][str(h)]['R_MS'];factor=g2**(power//2)
                values['VVSS'][h][0]+=factor*(q(line[1])+q(line[3])*mp.log(g2));values['VVSS'][h][1]+=factor*q(line[2])
        if role=='primary':total=[[mp.fsum(v[h][k] for v in values.values()) for k in range(3)] for h in range(3)]
        else:
            # Group scalar-only, mixed and vector/ghost sectors first; no
            # coupling prefactor or reference scale changes during addition.
            sectors=[['SSSS','SSS'],['VVSS','VSS','VVS','ghostS'],['VVVV','VVV','ghostV']]
            total=[[mp.fsum(mp.fsum(values[n][h][k] for n in names) for names in sectors) for k in range(3)] for h in range(3)]
        direct=[mp.fsum(v[h][0]+mp.mpf(2)/7*v[h][1]+(mp.mpf(2)/7)**2*v[h][2] for v in values.values()) for h in range(3)]
        assert all(abs(v[2])<mp.mpf('1e-80') for v in total)
        out[gskey]={'family_L_polynomials':{n:[[fmt(x) for x in v] for v in rows] for n,rows in values.items()},
          'known_graph_local_finite_L0':list(map(fmt,[r[0] for r in total])),'known_graph_local_scale_linear':list(map(fmt,[r[1] for r in total])),
          'raw_quadratic_sum':list(map(fmt,[r[2] for r in total])),'direct_at_L_2_over7':list(map(fmt,direct)),
          'finite_physical_C1':False,'unassembled_remainder':'Cparent-sum(original Cfamily) plus correlated finite/EFT/normalization/conversion terms'}
    return out

def forest_weight():
    C,G,P,x,y,px,py=s.symbols('C G P x y px py')
    marked=-C*(px*y+x*py)/8;kernel=-C*P/2;trace=G*kernel/2
    assert s.expand(marked.subs({x:G,y:G,px:P,py:P})-trace)==0
    assert trace!=-C*G*P/8 and 3*trace!=trace
    return {'proper_subgraphs':[[0],[1]],'proper_joint_forest_allowed':False,'single_vertex_overlap':True,
      'marked_sum':str(marked),'real_trace_insertion':str(trace),'two_markings_equal_one_full_real_trace':True,
      'overall_local_double_contraction_not_added_as_proper_forest':True}

def ownership(src,Q):
    v3,gv,vss,vr,vvs,gs,vs,s4,s3=src
    return {'quartic_CT_full_positive_d':[v['original_CT_full_positive_d'] for v in Q],
      'quartic_CT_internal_light_positive_d':[v['original_CT_light_positive_d'] for v in Q],
      'VVV':{k:v3[k] for k in ['forest_full_prefactor_H','forest_soft_prefactor_H','forest_hard_before_limit','forest_hard_limit']},
      'ghostV':{k:gv[k] for k in ['forest_full_prefactor_H','forest_soft_prefactor_H','forest_hard_before_limit','forest_hard_limit']},
      'SSSS':{k:s4[k] for k in ['original_Cfull','Csoft','Chard']},
      'SSS':{'source':'canonical_so10_scalar_cubic_amplitude tables/full_original_forest_blueprint','cuts':4806,'original_soft_closings':234},
      'VVSS':'both scalar_UV_CT and vector_UV_CT per coupling power retained in bound amplitude tables',
      'VSS':'all five qualified branch original forests retained; full closed parent-minus-family trace not assembled here',
      'ghostS':'qualified full original SCK three-cut forest before scalar-soft cancellation',
      'VVS':'qualified full original VVK three-cut forest before scalar/vector-soft cancellation',
      'Cparent_minus_sum_original_Cfamily_evaluated':False,'finite_physical_jets_or_overall_CT_adopted':False}
