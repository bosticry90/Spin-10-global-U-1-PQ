"""GSA1 complete actual positive-unit set; analytic vs finite-bubble routes."""
from data import *
def sck_helpers():
    source=CAL/'canonical_so10_spinzero_cubic_kernel'
    old=load('gsa_sck_data',source/'data.py');saved=sys.modules.get('data')
    try:
        sys.modules['data']=old;mod=load('gsa_sck_functions',source/'functions.py')
    finally:
        if saved is None:sys.modules.pop('data',None)
        else:sys.modules['data']=saved
    return old,mod
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin('units_preparation.json',600);mp.mp.dps=110
    rec=json.loads((HERE/'measure_receipt.json').read_bytes());assert rec['status']=='QUALIFIED_COMPLETE_GHOST_SCALAR_SPECTRAL_MEASURE'
    keys=sorted(set().union(*(set(v['positive_keys']) for v in rec['workload'].values())))
    softkeys=sorted(set().union(*(set(v['soft_keys']) for v in rec['workload'].values())))
    old,func=sck_helpers();master=old.old_master() if role=='primary' else None;compiled={};fallbacks=0
    if role=='primary':
        src=CAL/'canonical_so10_r3_scalar_current';raw=gzip.decompress((src/'analytic_derivatives_v10_tables.json.gz').read_bytes())
        receipt=json.loads((src/'backend_receipt_v10.json').read_bytes());assert sha256(raw).hexdigest()==receipt['tables_sha256']
        tab=json.loads(raw);assert tab['status']=='QUALIFIED_POSITIVE_MASS_MASTER_ANALYTIC_DERIVATIVE_BACKEND'
        xx,yy,zz,II=s.symbols('x y z Ifin',positive=True);loc={'x':xx,'y':yy,'z':zz,'Ifin':II}
        for token in ['300','030','003']:
            pair=tab['functions'][token];f=s.sympify(pair[0],locals=loc)*II+s.sympify(pair[1],locals=loc)
            compiled[token]=s.lambdify([xx,yy,zz,II],f,modules='mpmath',cse=True)
    positive={};maxquad=mp.mpf(0);maxleak=mp.mpf(0)
    for ni,key in enumerate(keys):
        x,z=map(mp.mpf,key.split('|'));masses=[x,mp.mpf(1),z];values=[];hist=[]
        if role=='primary':
            X,Y,Z=masses;lam=X*X+Y*Y+Z*Z-2*X*Y-2*X*Z-2*Y*Z
            guarded=abs(lam)/(1+X+Y+Z)**2<=mp.mpf('1e-20')
            if guarded:fallbacks+=1
            base=None if guarded else master.sunset(*masses,q2=1,method='dilog')
            for axis,token in enumerate(['300','030','003']):
                d3=master.imaster_derivative(tuple(map(str,masses)),tuple(map(int,token))) if guarded else compiled[token](*masses,base)
                value=masses[axis]*d3/6;maxleak=max(maxleak,abs(mp.im(value))/(1+abs(value)));assert maxleak<mp.mpf('1e-80')
                values.append(mp.re(value))
        else:
            for axis in range(3):
                history=[]
                for degree in [8,10]:
                    value,estimate=func.bubble_unit(masses[axis],masses[(axis+1)%3],masses[(axis+2)%3],degree)
                    assert estimate<mp.mpf('1e-50');history.append({'maxdegree':degree,'value':mp.nstr(value,85),'error_estimate':mp.nstr(estimate,15)})
                change=abs(mp.mpf(history[0]['value'])-mp.mpf(history[1]['value']))/(1+abs(value));maxquad=max(maxquad,change);assert change<mp.mpf('1e-45')
                values.append(value);hist.append(history)
        positive[key]={'masses':list(map(str,masses)),'finite':[mp.nstr(v,75) for v in values],
          'pole':['0']*3,'scale':[mp.nstr(-1/(6*v),85) for v in masses]}
        if role=='replay':positive[key]['quadrature_histories']=hist
        if ni%10==9:print('STAGE '+role+'_complete_positive_units_'+str(ni+1),flush=True)
    soft={};src=CAL/'canonical_so10_spinzero_cubic_kernel'
    for key in softkeys:
        x,z=map(mp.mpf,key.split('|'));assert z==0 and abs(x-mp.mpf(3)/253)<mp.mpf('1e-75')
        if role=='primary':
            tab=packed(src/'primary_numeric_numeric_v1_tables.json.gz')['soft']['2']
            vals=[mp.mpf(h[-1]['value']) for h in tab['heavy_axes']]+[mp.mpf(tab['scalar_axis'][-1]['Laurent'][2])]
            kinetic=mp.mpf(tab['kinetic_direct_quad'])
        else:
            tab=packed(src/'replay_soft2_numeric_v1_tables.json.gz')['data'];assert tab['ratio']=='3/253'
            vals=[mp.mpf(axis['scales'][0]['matched']) for axis in tab['histories'][-1]['axes']]
            kinetic=func.kinetic(mp.mpf(3)/253)
        soft[key]={'finite':[mp.nstr(v,75) for v in vals],'pole':['0']*3,
          'scale':[mp.nstr(-1/(6*x),85),mp.nstr(-mp.mpf(1)/6,85),'0'],'kinetic_K':mp.nstr(kinetic,85),
          'source':'QUALIFIED_SCK1_COMPLETE_HISTORIES_REUSED_NOT_RERUN'}
    out={'schema':'GSA1_COMPLETE_UNITS','role':role,'positive':positive,'soft':soft,'working_digits':110,
      'positive_count':len(positive),'soft_count':len(soft),'analytic_Kallen_fallbacks':fallbacks,
      'max_quad_scaled_change':mp.nstr(maxquad,30),'max_scaled_imaginary_leak':mp.nstr(maxleak,30),
      'scientific_acceptance':'NOT_PERFORMED','full_model_amplitude_qualified':False}
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_units_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'kind':'units','elapsed_after_imports':time.perf_counter()-start,
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
if __name__=='__main__':main()
