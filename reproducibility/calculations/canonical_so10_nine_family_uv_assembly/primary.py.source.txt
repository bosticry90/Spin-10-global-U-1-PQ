"""G2P1 actual quartic pole-matrix closure and native nine-family assembly."""
from data import *
start=begin();mp.mp.dps=110;Q,src,poles=assemble('primary')
save('primary',{'schema':'G2P1_NINE_FAMILY_COMBINATION','quartic':Q,'pole_assembly':poles,'finite_cases':finite_cases('primary',Q,src),
 'quartic_forest_weight':forest_weight(),'original_forest_ownership':ownership(src,Q),
 'RG_comparator_answer_read':False,'full_C1_or_E5_qualified':False},start)
