"""S3A1 actual row/group contractions and independent inverse slope."""
from pathlib import Path
from hashlib import sha256
from collections import defaultdict
import json,gzip,sys,time,threading,os,importlib.util
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def begin(prep='preparation.json'):
    start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def fmt(v):return mp.nstr(mp.re(v),65)
def save(role,value,start):
    raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),
      'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def q(v):
    a,sep,b=str(v).partition('/');return mp.mpf(a)/mp.mpf(b) if sep else mp.mpf(a)
def inputs(role):
    measure=packed(CAL/'canonical_so10_scalar_cubic_spectral_measure'/f'{role}_tables.json.gz')
    charges=packed(CAL/'canonical_so10_scalar_quartic_charge_projection'/f'{role}_tables.json.gz')['class_values']
    units={}
    for p in sorted((CAL/'canonical_so10_scalar_cubic_units').glob(role+'_*_tables.json.gz')):
        for v in packed(p)['tasks']:assert v['index'] not in units;units[v['index']]=v
    tasks=json.loads((CAL/'canonical_so10_scalar_cubic_units/task_catalog.json').read_bytes());assert len(tasks)==len(units)==956
    lookup={(v['case'],tuple(v['mass_keys'])):v['index'] for v in tasks}
    return measure,charges,units,tasks,lookup
def aggregate(role,gs):
    measure,charges,units,tasks,lookup=inputs(role);case='1/2' if gs==mp.mpf('.5') else '1';total=[mp.mpf(0)]*3;slope=total[:];direct=total[:]
    domains={str(i):total[:] for i in range(3)};controls={n:total[:] for n in ['wrong_axis_permutation','delete_soft_domains','omit_soft_kinetic','blind_Q1_reference','extra_g2_prefactor','omit_overlap_at_delta_over_M_1e-20','omit_overlap_at_delta_over_M_1e-40']}
    grouped={};forest=defaultdict(lambda:[mp.mpf(0)]*3);blueprint=[]
    for row in measure['rows']:
        if row['classification']!='KERNEL_REQUIRED':continue
        keys=tuple(row['mass_keys'][a] for a in row['sorted_axes']);tag=case if any(k.startswith('G:') for k in keys) else 'fixed';index=lookup[tag,keys];unit=units[index];values=list(map(q,unit['finite_L0']));scales=list(map(q,unit['scale']));mass=list(map(q,unit['masses']))
        cls=row['classes'];pref=q(row['class_orbit'])*q(row['weight'])/2;soft=row['types'].count(1)
        weights=[[pref*q(charges[h][cls[a]]) for a in range(3)] for h in range(3)]
        for h in range(3):
            fv=mp.fsum(weights[h][a]*values[row['inverse_axes'][a]] for a in range(3));sv=mp.fsum(weights[h][a]*scales[row['inverse_axes'][a]] for a in range(3))
            domains[str(soft)][h]+=fv
            if role=='primary':
                total[h]+=fv;slope[h]+=sv;direct[h]+=mp.fsum(weights[h][a]*(values[row['inverse_axes'][a]]+mp.mpf(2)/7*scales[row['inverse_axes'][a]]) for a in range(3))
            controls['wrong_axis_permutation'][h]+=mp.fsum(weights[h][a]*(values[a]-values[row['inverse_axes'][a]]) for a in range(3))
            if soft:controls['delete_soft_domains'][h]-=fv
            for a,t in enumerate(row['types']):
                if t==1 and soft:controls['omit_soft_kinetic'][h]-=weights[h][a]*values[row['inverse_axes'][a]]/3
                if t==1 and soft==2:
                    M=next(v for v in mass if v)
                    for exponent in [20,40]:controls['omit_overlap_at_delta_over_M_1e-'+str(exponent)][h]+=weights[h][a]*exponent*mp.log(10)/(6*M)
            controls['blind_Q1_reference'][h]-=mp.log(60)*sv
        if index not in grouped:grouped[index]=[[[] for a in range(3)] for h in range(3)]
        for h in range(3):
            for j,a in enumerate(row['sorted_axes']):grouped[index][h][j].append(weights[h][a])
        for axis,key in enumerate(row['mass_keys']):
            coeff=[weights[h][axis]/6 for h in range(3)]
            for h in range(3):forest[key][h]+=coeff[h]
            blueprint.append({'classes':cls,'mode_ids':row['mode_ids'],'axis':axis,'closing_mass_key':key,
              'original_common_delta_closing':row['types'][axis]==1,'coefficient_of_Hm_over_m_epsilon':list(map(fmt,coeff))})
    if role=='replay':
        for index,W in grouped.items():
            unit=units[index];values=list(map(q,unit['finite_L0']));scales=list(map(q,unit['scale']))
            for h in range(3):
                ww=[mp.fsum(v) for v in W[h]];total[h]+=mp.fsum(ww[a]*values[a] for a in range(3));slope[h]+=mp.fsum(ww[a]*scales[a] for a in range(3));direct[h]+=mp.fsum(ww[a]*(values[a]+mp.mpf(2)/7*scales[a]) for a in range(3))
    for h in range(3):controls['extra_g2_prefactor'][h]=(gs-1)*total[h]
    return {'finite_L0':list(map(fmt,total)),'scale_linear':list(map(fmt,slope)),'direct_L_2_over7':list(map(fmt,direct)),
      'finite_by_soft_count':{k:list(map(fmt,v)) for k,v in domains.items()},'controls':{k:list(map(fmt,v)) for k,v in controls.items()},
      'original_forest_by_closing_mass':{k:list(map(fmt,v)) for k,v in sorted(forest.items())},'full_original_forest_blueprint':blueprint}

def inverse_slope(role):
    spec=importlib.util.spec_from_file_location('s3a_mass_data',CAL/'canonical_so10_scalar_cubic_spectral_measure/data.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    frame,grams,charges,fci,blocks,counts=M.exact_inputs(role);root=M.root_value(role);physical=[];gold=[];error=mp.mpf(0)
    for block in blocks:
        H=M.numeric(block['H'],root);P=M.numeric(block['P'][0],root);PH=(H+mp.eye(H.rows)-P)**-1*P
        PG=sum((M.numeric(block['P'][j+2],root)/q(v) for j,v in enumerate(['3/10','3/2','25','253/10'])),mp.zeros(H.rows))
        error=max(error,M.norm(H*PH-P)/(1+M.norm(H)),M.norm(PH-PH.H));physical.append(PH);gold.append(PG)
    assert error<mp.mpf('1e-70');A=[mp.mpf(0)]*3;B=A[:]
    for g in grams['groups']:
        cls=g['classes'];entries=M.gram_entries(g);pref=-mp.mpf(M.orbit(cls))/12
        for axis,c in enumerate(cls):
            As=[mp.eye(m) for m in g['shape']];As[axis]=physical[c];v=M.gtrace(entries,As);As[axis]=gold[c];z=M.gtrace(entries,As)
            for h in range(3):A[h]+=pref*q(charges[h][c])*v;B[h]+=pref*q(charges[h][c])*z
    return {'constant_A':list(map(fmt,A)),'inverse_g2_B':list(map(fmt,B)),'pseudoinverse_max_scaled_residual':fmt(error)}
