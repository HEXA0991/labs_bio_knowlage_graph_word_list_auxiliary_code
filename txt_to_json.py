import json
import codecs as cs

path_old = r'C:\Users\dell\Desktop\huop\原本词表\原本词表\Organization_nospaceend.txt'
path_new = r'C:\Users\dell\Desktop\huop\原本词表\原本词表\Organization.json'

fp_old = cs.open(path_old,'r','utf-8')
contents = fp_old.readlines()
fp_old.close()

ents = [] #存放实体-ID 对
for cont in contents:
    ents.append(cont.strip('\r\n').split('***'))

json_dict = {} #空的json字典
for ent in ents:
    for word in ent[1].split('|'):
        json_dict[word] = ent[0]

json_data = json.dumps(json_dict)

fp_new = cs.open(path_new,'w','utf-8')
fp_new.write(json_data)
fp_new.close()

pass 


