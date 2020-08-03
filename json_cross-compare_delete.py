import codecs as cs
import json
from itertools import product  #使用笛卡尔积生成介词的替换列表

class count: #定义一个迭代器类作为循环计数器
    def __init__(self, max):
        self.maximum = max

    def __iter__(self):
        self.cnt = 0
        return self

    def __next__(self):
        x = self.cnt
        self.cnt = (self.cnt + 1) % self.maximum
        return x
    
    def get(self):
        return self.cnt



preposition = ['the','The','of','and','at','on','&','from','to',''] #几种常见介词，在匹配时可以进行模糊匹配

path_old = r'C:\Users\dell\Desktop\huop\原本词表\原本词表\Organization.json' #旧词表路径
path_new = r'C:\Users\dell\Desktop\huop\审过\Organization_no_blank_row.txt' #待核对词表路径
path_log = r'C:\Users\dell\Desktop\huop\审过\Organization_json_log.txt' #日志文件路径
path_done = r'C:\Users\dell\Desktop\huop\审过\Organization_done.txt' #输出结果路径

fp_old = cs.open(path_old,'r','utf-8')
json_dic = json.load(fp_old) #读取旧词表的 json 文件
fp_old.close()

fp_new = cs.open(path_new,'r','utf-8')
entrys = fp_new.readlines() #存放文件里的每一个条目
fp_new.close()

ents = [] #存放所有实体单元
for entry in entrys:
    ents.append(entry.strip('\r\n').split('|'))

fp_log = cs.open(path_log,'w','utf-8')
#以新词表中实体为键在旧词表的词典里进行匹配
for ent_num in range(len(ents)):
    for word_num in range(len(ents[ent_num])):
        if ents[ent_num][word_num] in json_dic: #如果新词表中实体在旧词表中有严格匹配，则应该删除这个实体，如果这个实体之后有相同实体，则都为同义实体，后面加ID
            temp = ents[ent_num][word_num] #暂时保存新词表中的实体，以防删除之后丢失
            del ents[ent_num][word_num]
            fp_log.write('delete\t' + temp + '\t' + str(ent_num) + '\t' + str(word_num) + json_dic[temp] + '\n')
            if ents[ent_num]: #如果列表中还有其他实体，则都是同义实体，后面加ID
                ents[ent_num].append('**' + json_dic[temp])
            break #此行实体当作全部处理完毕，开始处理下一行实体
        else:
            if ' ' in ents[ent_num][word_num]: #如果实体中含空格，则代表实体由多个单词组成，可能要模糊匹配
                temp = ents[ent_num][word_num].split(' ') #保存分隔后实体中每个词
                pre_pos = [] #存储介词的位置
                for i in range(len(temp)): #寻找介词的位置，同时将每个单词首字母变大写，因为词表中所有条目都是大写
                    if temp[i] in preposition:
                        pre_pos.append(i)
                    else:
                        temp[i] = temp[i].capitalize()
                temp_str = '' #暂时存放拼接字符串
                for ele in temp:
                    temp_str += ele + ' '
                temp_str = temp_str.strip(' ') #删除最后一个不需要的空格
                if temp_str in json_dic: #如果直接有匹配
                    ents[ent_num].append('**' + json_dic[temp_str]) #是同义实体，后面加ID
                    fp_log.write('match\t' + ents[ent_num][word_num] + '\t' +str(ent_num) + '\t' + str(word_num) + '\t' + json_dic[temp_str] + '\n')
                    break #此行实体当作全部处理完毕，开始处理下一行实体
                else: #开始使用介词代换的模糊匹配
                    if len(pre_pos) > 6: #旧词表中单个实体最多只有 6 个介词，因此如果待匹配实体中介词超过 6 个就不进行比较，大大节省时间
                        continue
                    pre_replace = list(product(preposition, repeat= len(pre_pos)))
                    temp_str = '' #清空字符串缓存
                    cnt = count(len(pre_pos)) #设立迭代器当作计数器
                    cnt = iter(cnt)
                    match = 0 #此行实体是否被匹配的标志位
                    for pre_ruple in pre_replace: #对此实体中的每个介词的位置进行介词代换，寻找同义项
                        temp_str = '' #清空字符串缓存
                        for pos in range(len(temp)): #对这个实体每个词进行遍历
                            if pos in pre_pos: #如果这个词是介词
                                if pre_ruple[cnt.get()] == '': #如果此介词位置这次不需要添加介词，进行下义词循环
                                    continue
                                else:
                                    temp_str = temp_str + pre_ruple[next(cnt)] + ' ' #将介词拼接到这个位置
                            else:
                                temp_str = temp_str + temp[pos] + ' '
                        temp_str = temp_str.strip(' ') #删除最后一个不需要的空格
                        if temp_str in json_dic: #如果有匹配
                            ents[ent_num].append('**' + json_dic[temp_str]) #是同义实体，后面加ID
                            fp_log.write('match\t' + ents[ent_num][word_num] + '\t' +str(ent_num) + '\t' + str(word_num) + '\t' + json_dic[temp_str] + '\n')
                            match = 1 #实体被匹配
                            break #跳出这个实体的循环
                    if match == 1: #如果此行实体有一个被匹配
                        break #跳出这一行的循环     
            else: #只剩下不能匹配的缩写，直接进行下一次循环
                continue
fp_log.close()

#将完成的文件输入新文件
fp_done = cs.open(path_done,'w','utf-8')
for ent_num in range(len(ents)):
    for word_num in range(len(ents[ent_num])):
        if ents[ent_num][word_num] == '': #如果一行为空则代表这一行没有内容，直接跳出循环，这个判断都不需要有，因为list为空是不会进行循环的
            break
        elif ents[ent_num][word_num][0] == '*': #如果第一个字符是 * 代表这个元素是ID
            fp_done.write(ents[ent_num][word_num])
        else: #否则代表这个元素是实体
            try:
                if ents[ent_num][word_num + 1] and ents[ent_num][word_num + 1][0] != '*': #判断这个实体之后还有没有实体，如果有实体是不是 * 开头
                    fp_done.write(ents[ent_num][word_num] + '|') #如果有且不是ID则后面要加分隔符
                else: #否则后面是ID，不加分隔符
                    fp_done.write(ents[ent_num][word_num])
            except:
                fp_done.write(ents[ent_num][word_num])
    if ents[ent_num]: #如果此行有内容则回车转行
        fp_done.write('\r\n')
    
fp_done.close()


pass


