"""G2P1 independent completed QUS closure and grouped common-scale assembly."""
from data import *
start=begin();mp.mp.dps=140;Q,src,poles=assemble('replay')
save('replay',{'schema':'G2P1_NINE_FAMILY_COMBINATION','quartic':Q,'pole_assembly':poles,'finite_cases':finite_cases('replay',Q,src),
 'quartic_forest_weight':forest_weight(),'original_forest_ownership':ownership(src,Q),
 'RG_comparator_answer_read':False,'full_C1_or_E5_qualified':False},start)
