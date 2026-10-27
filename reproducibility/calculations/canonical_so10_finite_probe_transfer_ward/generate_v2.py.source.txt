from pathlib import Path
O=Path(__file__).resolve().parent
x=(O/'native.py').read_text(encoding='utf-8')
x=x.replace('[[i,j,str(v)] for','[[int(i),int(j),str(v)] for',1).replace("read(O/'preparation.json')","read(O/'continuation_preparation_v2.json')",1).replace("(O/(role+'_tables.json.gz'))","(O/('replay_v2_tables.json.gz'))",1)
with(O/'native_v2.py').open('x',encoding='utf-8',newline='\n') as f:f.write(x)
x=(O/'verify.py').read_text(encoding='utf-8').replace('validation_preparation.json','validation_preparation_v2.json').replace("['primary','replay']","['primary','replay_v2']")
with(O/'verify_v2.py').open('x',encoding='utf-8',newline='\n') as f:f.write(x)
print('GENERATED_V2_SERIALIZATION_ONLY')
