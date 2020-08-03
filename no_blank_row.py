import codecs as cs

fp = cs.open(r'C:\Users\dell\Desktop\huop\审过\Organization_no_space_end.txt','r','utf-8')
fp_w = cs.open(r'C:\Users\dell\Desktop\huop\审过\Organization_no_blank_row.txt','w','utf-8')
ents = fp.readlines()
fp.close()

for ent in ents:
    if not(ent == '\r\n'):
        fp_w.write(ent)
fp_w.close()