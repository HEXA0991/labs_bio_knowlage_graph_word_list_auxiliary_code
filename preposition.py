import codecs as cs


path_r = r'C:\Users\dell\Desktop\huop\审过\Organization.txt' #工作文件
path_w = r'C:\Users\dell\Desktop\huop\审过\Organization_preposition.txt' #结果文件
path_log = r'C:\Users\dell\Desktop\huop\审过\Organization_log.txt' #日志文件

preposition = []

low_case = [] #存储所有小写

fp_r = cs.open(path_r,'r','utf-8')
entrys = fp_r.readlines() #存放文件里的每一个条目
fp_r.close()
entity_list = [] #存放所有实体单元
for entry in entrys:
    entity_list= entry.strip('\r\n').split('|') + entity_list

for ele in entity_list:
    temp = ele.split(' ')
    for word in temp:
        try:
            if not(word[0] >= 'A' and word[0] <= 'Z') and (word not in preposition):
                preposition.append(word)
        except:
            continue #如果实体后面有空格则会产生index error

fp_w = cs.open(path_w,'w','utf-8')
for ele in preposition:
    fp_w.write(ele + '\n')

pass