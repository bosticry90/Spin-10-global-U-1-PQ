"""Interpret actual omission controls and preserve insensitive projections."""
from data import *
def main():
    start=begin('controls_preparation.json',300);mp.mp.dps=110
    v=json.loads((HERE/'validation_receipt.json').read_bytes());assert v['status']=='QUALIFIED_COMPLETE_COMMON_SCALE_GHOST_SCALAR_PRIMITIVE'
    g=packed(CAL/'canonical_so10_ghost_scalar_charge_kernel/primary_tables.json.gz')
    assert all(row[1]==0 for row in g['averaged_Casimir_change_positions'].values())
    out={}
    for gs,c in v['cases'].items():
        full=list(map(mp.mpf,c['finite_L0']));parts={k:list(map(mp.mpf,row)) for k,row in c['finite_parts'].items()}
        omissions={}
        for omit in ['Gold','soft']:
            kept=[sum(parts[k][i] for k in parts if k!=omit) for i in range(3)]
            delta=[kept[i]-full[i] for i in range(3)]
            for i in range(3):assert abs(delta[i]+parts[omit][i])<mp.mpf('1e-45')*(1+abs(full[i]))
            assert max(abs(a) for a in delta)>mp.mpf('1e-12')
            omissions['omitted_'+omit+'_finite_change']=[mp.nstr(a,45) for a in delta]
        average=list(map(mp.mpf,c['controls']['averaged_ghost_Casimir']));kin=list(map(mp.mpf,c['controls']['missing_soft_kinetic']))
        assert abs(average[1])<mp.mpf('1e-60') and abs(average[0])>mp.mpf('1e-8') and abs(average[2])>mp.mpf('1e-8')
        assert kin[2]==0 and kin[0]>mp.mpf('1e-12') and kin[1]>mp.mpf('1e-12')
        omissions.update({'SU2_averaged_ghost_Casimir':'INSENSITIVE: exact GSK charge matrices already scalar on each mass sector',
          'SU3_soft_kinetic':'INSENSITIVE: exact zero scalar-soft charge',
          'UV_poles_for_finite_mutations':'INSENSITIVE: all proper unit overall poles are zero'})
        out[gs]=omissions
    result={'schema':'GSA1_CONTROL_INTERPRETATION','status':'QUALIFIED_COMPLETE_FINITE_OMISSION_CONTROLS',
      'primary_scientific_receipt_sha256':sha256((HERE/'validation_receipt.json').read_bytes()).hexdigest(),
      'cases':out,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'elapsed_after_imports':time.perf_counter()-start}
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    with (HERE/'control_receipt.json').open('xb') as f:f.write(raw)
    print('RESULT '+json.dumps({'receipt_filename':'control_receipt.json','receipt_sha256':sha256(raw).hexdigest(),
      'elapsed_after_imports':result['elapsed_after_imports']},sort_keys=True),flush=True)
if __name__=='__main__':main()
