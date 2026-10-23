"""VVA1 every actual unit: analytic derivative vs convergent bubble evaluation."""
from data import *
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin('units_preparation.json');mp.mp.dps=110
    measure=packed(HERE/'combined_measure_tables.json.gz');wanted={t:sorted(set().union(*(set(v[t]) for v in measure['workload'].values()))) for t in ['positive','soft','light']}
    vd,fun=kernel_helpers();old,sf=fun.sck();master=old.old_master() if role=='primary' else None
    cached=packed(CAL/'canonical_so10_ghost_scalar_sunset/replay_units_tables.json.gz')['positive'];compiled={};fallbacks=0;cachecount=0
    if role=='primary':
        src=CAL/'canonical_so10_r3_scalar_current';blob=gzip.decompress((src/'analytic_derivatives_v10_tables.json.gz').read_bytes());rec=json.loads((src/'backend_receipt_v10.json').read_bytes());assert sha256(blob).hexdigest()==rec['tables_sha256'];tab=json.loads(blob)
        X,Y,Z,II=s.symbols('x y z Ifin',positive=True);loc={'x':X,'y':Y,'z':Z,'Ifin':II}
        for token in ['200','020','110','300','030','003']:
            pair=tab['functions'][token];expr=s.sympify(pair[0],locals=loc)*II+s.sympify(pair[1],locals=loc)
            compiled[token]=s.lambdify([X,Y,Z,II],expr,modules='mpmath',cse=True)
    result={t:{} for t in wanted};maxref=mp.mpf(0);maxleak=mp.mpf(0)
    for no,key in enumerate(wanted['positive']):
        x,z=map(mp.mpf,key.split('|'));m=[x,mp.mpf(1),z];history=[]
        if role=='primary':
            lam=x*x+1+z*z-2*x-2*x*z-2*z;guard=abs(lam)/(1+x+z)**2<=mp.mpf('1e-20');fallbacks+=guard
            base=None if guard else master.sunset(*m,q2=1,method='dilog');der={}
            for token,f in compiled.items():
                value=master.imaster_derivative(tuple(map(str,m)),tuple(map(int,token))) if guard else f(*m,base)
                maxleak=max(maxleak,abs(mp.im(value))/(1+abs(value)));assert maxleak<mp.mpf('1e-80');der[token]=mp.re(value)
            values=[2*x*der['300']/3+4*(der['200']+der['110']),2*der['030']/3+4*(der['020']+der['110']),2*z*der['003']/3-4*der['110']+1/(3*z)]
        else:
            reuse=key in cached;cachecount+=reuse
            for md in [8,10]:
                rs=list(map(mp.mpf,cached[key]['finite'])) if reuse else [sf.bubble_unit(m[k],m[(k+1)%3],m[(k+2)%3],md)[0] for k in range(3)]
                xx,ex=fun.xx_unit(x,1,z,md);yy,ey=fun.xx_unit(1,x,z,md);xy,ec=fun.xy_unit(x,1,z,md)
                error=max(ex,ey,ec);assert error<mp.mpf('1e-50')
                values=[4*rs[0]+4*(xx+xy),4*rs[1]+4*(yy+xy),4*rs[2]-4*xy+1/(3*z)]
                history.append({'maxdegree':md,'finite':[mp.nstr(v,85) for v in values],'spin_quad_error_estimate':mp.nstr(error,20)})
            change=max(abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b))) for a,b in zip(history[0]['finite'],history[1]['finite']));maxref=max(maxref,change);assert change<mp.mpf('1e-45')
        result['positive'][key]={'finite':[mp.nstr(v,75) for v in values],'pole':['0']*3,'scale':[mp.nstr(10/(3*x),85),mp.nstr(mp.mpf(10)/3,85),mp.nstr(-2/(3*z),85)]}
        if role=='replay':result['positive'][key].update({'histories':history,'scalar_unit_reused':reuse})
        if no%10==9:print('STAGE '+role+'_positive_units_'+str(no+1),flush=True)
    src=CAL/'canonical_so10_two_vector_cubic_kernel'
    for key in wanted['soft']:
        r,z=map(mp.mpf,key.split('|'));assert z==0 and abs(r-mp.mpf(3)/253)<mp.mpf('1e-75')
        if role=='primary':vals=packed(src/'primary_numeric_tables.json.gz')['scalar_soft']['0']['history'][-1]['finite']
        else:vals=packed(src/'replay_scalar0_numeric_tables.json.gz')['histories'][-1]['scales'][0]['matched']
        K=sf.kinetic(r);result['soft'][key]={'finite':[mp.nstr(mp.mpf(v),75) for v in vals],'pole':['0']*3,
          'scale':[mp.nstr(10/(3*r),85),mp.nstr(mp.mpf(10)/3,85),'0'],'K':mp.nstr(K,85),'source':'QUALIFIED_VCK1_REUSED'}
    for key in wanted['light']:
        assert key=='0|1'
        if role=='primary':vals=[row[2] for row in packed(src/'primary_numeric_tables.json.gz')['vector_soft'][0]['Gamma'][-1]['Laurent']]
        else:vals=packed(src/'replay_vector_numeric_tables.json.gz')['histories'][-1]['scales'][0]['matched']
        result['light'][key]={'finite':[mp.nstr(mp.mpf(v),75) for v in vals],'pole':['-2/3','-2','2'],'scale':['-4/3','-2/3','10/3'],'source':'QUALIFIED_VCK1_REUSED'}
    save(role,'units',{'schema':'VVA1_UNITS',**result,'working_digits':110,'Kallen_fallbacks':fallbacks,
      'qualified_scalar_unit_reuse_count':cachecount,'max_refinement':mp.nstr(maxref,30),'max_imaginary_leak':mp.nstr(maxleak,30),
      'scientific_acceptance':'NOT_PERFORMED'},start)
if __name__=='__main__':main()
