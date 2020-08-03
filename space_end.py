import codecs as cs

fp = cs.open(r'C:\Users\dell\Desktop\huop\原本词表\原本词表\Organization.txt','r','utf-8')
fp_w = cs.open(r'C:\Users\dell\Desktop\huop\原本词表\原本词表\Organization_nospaceend.txt','w','utf-8')
ents = fp.readlines()
fp.close()

entitys = []
for ent in ents:
    entitys.append(ent.strip('\r\n'))

stripped = []
for entity in entitys:
    stripped.append(entity.strip(' '))

for s in stripped:
    fp_w.write(s + '\r\n')
fp_w.close()