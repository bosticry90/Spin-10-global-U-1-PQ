"""Explicit scalar-error histories for the2 actual non-reused positive keys."""
from data import *
def main():
    start=begin('scalar_estimates_preparation.json');mp.mp.dps=110
    A=packed(HERE/'primary_units_tables.json.gz');B=packed(HERE/'replay_units_tables.json.gz');vd,fun=kernel_helpers();old,sf=fun.sck()
    keys=[k for k,v in B['positive'].items() if not v['scalar_unit_reused']];assert len(keys)==2
    maxerr=mp.mpf(0);maxref=mp.mpf(0);maxunit=mp.mpf(0);histories={}
    for key in keys:
        x,z=map(mp.mpf,key.split('|'));m=[x,mp.mpf(1),z];hist=[]
        for md in [8,10]:
            scalar=[sf.bubble_unit(m[i],m[(i+1)%3],m[(i+2)%3],md) for i in range(3)]
            assert max(v[1] for v in scalar)<mp.mpf('1e-50');maxerr=max(maxerr,*[v[1] for v in scalar])
            xx,ex=fun.xx_unit(x,1,z,md);yy,ey=fun.xx_unit(1,x,z,md);xy,ec=fun.xy_unit(x,1,z,md)
            assert max(ex,ey,ec)<mp.mpf('1e-50')
            values=[4*scalar[0][0]+4*(xx+xy),4*scalar[1][0]+4*(yy+xy),4*scalar[2][0]-4*xy+1/(3*z)]
            for table in [A,B]:
                for v,w in zip(values,table['positive'][key]['finite']):
                    er=abs(v-mp.mpf(w))/(1+abs(v));maxunit=max(maxunit,er);assert er<mp.mpf('1e-40')
            hist.append({'maxdegree':md,'scalar_values':[mp.nstr(v[0],85) for v in scalar],'scalar_error_estimates':[mp.nstr(v[1],25) for v in scalar]})
        for a,b in zip(hist[0]['scalar_values'],hist[1]['scalar_values']):
            er=abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(b)));maxref=max(maxref,er);assert er<mp.mpf('1e-45')
        histories[key]=hist
    out={'status':'QUALIFIED_NEW_VVS_SCALAR_UNIT_ERROR_ESTIMATES','execution_state':'COMPLETED','keys':keys,'scalar_axes':6,'histories':histories,
      'max_error_estimate':mp.nstr(maxerr,30),'max_refinement':mp.nstr(maxref,30),'max_complete_unit_comparison':mp.nstr(maxunit,30),
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED','elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'scalar_estimate_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'receipt_filename':'scalar_estimate_receipt.json','receipt_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':out['elapsed_after_imports']},sort_keys=True),flush=True)
if __name__=='__main__':main()
