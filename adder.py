import codecs as cs

path = r'C:\Users\dell\Desktop\huop\审过'

content = []
fp = cs.open(path + '\\' + 'Organization_done.txt','r','utf-8')
content = fp.readlines()
fp.close()

stripped = []
for i in content:
    stripped.append(i.strip('\r\n') + '**\r\n')

fp_w = cs.open(path + '\\' + 'Organization_added.txt','w','utf-8')
for j in stripped:
    fp_w.write(j)

fp_w.close()