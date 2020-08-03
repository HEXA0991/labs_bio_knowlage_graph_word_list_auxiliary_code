import codecs as cs



#path_r = r'C:\Users\dell\Desktop\huop\审过\Organization_no_space_end.txt' #工作文件
#path_w = r'C:\Users\dell\Desktop\huop\审过\Organization_new.txt' #结果文件
#path_log = r'C:\Users\dell\Desktop\huop\审过\Organization_log.txt' #日志文件

path_r = r'C:\Users\dell\Desktop\huop\审过\Pathogen_no_space_end.txt' #工作文件
path_w = r'C:\Users\dell\Desktop\huop\审过\Organization_new.txt' #结果文件
path_log = r'C:\Users\dell\Desktop\huop\审过\Pathogen_acronym_log.txt' #日志文件

preposition = ['the','of','and','at','on','&','from','to',''] #按道理空字符串会在 30 行过滤，但是为了保险还是加上

fp_r = cs.open(path_r,'r','utf-8')
entrys = fp_r.readlines() #存放文件里的每一个条目
fp_r.close()

entity_list = [] #存放所有实体单元
for entry in entrys:
    entity_list.append(entry.strip('\r\n').split('|'))

acronym = [] #保存所有缩写位置
first_letter = [] #保存所有首字母及位置

#提取所有缩写 && 所有实体大写的首字母序列
list_num = 0 #条目序号
for list_num in range(len(entity_list)):
    ent_num = 0 #条目内实体序号
    for ent_num in range(len(entity_list[list_num])):
        if ' ' in entity_list[list_num][ent_num]: #如果这个实体中有空格则代表这个实体可以被分割
            temp = entity_list[list_num][ent_num].split(' ') #按照空格分隔
            temp_acro = '' #临时保留首字母大写
            for ele in temp:
                if not(ele[0] >= 'A' and ele[0] <= 'Z') and not(ele[0] >= 'a' and ele[0] <= 'z'): #如果首字母不是大写字母 && 首字母不是小写字母，代表这个单词不是需要保存的内容，继续循环
                    continue
                elif ele in preposition: #如果这个单词是介词则继续下一次循环
                    continue
                else: #这个词是大写 || 小写字母开头保存下来
                    if ele[0] >= 'A' and ele[0] <= 'Z': #如果首字母是大写则直接存储
                        temp_acro = temp_acro + ele[0]
                    else: #否则则需要转换为大写
                        ele = ele.capitalize()
                        temp_acro = temp_acro + ele[0]
            if temp_acro: #如果字符不为空则存储
                first_letter.append([temp_acro, list_num, ent_num])
            else: #为空则不需要存储
                continue
        else: #如果实体中没有空格，则可能是缩写或者带数字的缩写
            temp = entity_list[list_num][ent_num] #暂时存储这个元素
            if (temp[0] >= 'A' and temp[0] <= 'Z') and ('-' not in temp) and (temp[1] >= 'A' and temp[1] <= 'Z'): #缩写均为大写 && 单词中没有“-” && 单词全为大写字母
                acronym.append([temp, list_num, ent_num])
            else: #如果不是大写则代表这个元素不是实体
                continue

#开始匹配缩写和首字母
bingo = [] #存放匹配的缩写对[提取的缩写列表序号，提取的首字母列表序号]
for acro_num in range(len(acronym)): #固定缩写找首字母匹配
    for f_num in range(len(first_letter)):
        if acronym[acro_num][0] == first_letter[f_num][0]: #如果缩写和首字母匹配
            bingo.append([acro_num, f_num])

fp_log = cs.open(path_log,'w','utf-8')
for ele in bingo: #逐个输出到日志文件中
    quad = acronym[ele[0]][0] + '\t' + str(acronym[ele[0]][1] + 1) + '\t' + str(entity_list[first_letter[ele[1]][1]][first_letter[ele[1]][2]]) + '\t' + str(first_letter[ele[1]][1] + 1) + '\n'
    fp_log.write(quad)






pass #debug



