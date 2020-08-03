## space_end.py

将新词表中每行后面的空格删除



## preposition.py

将一个词表中所有实体中的非小写单词输出，以便人工筛选介词



## acronym.py

将可能的缩写和全称匹配

+ 需要用到 prepositon.py 生成的介词表
+ 可以自动将全称首字母大写后匹配
+ 可以忽略全称中介词进行匹配
+ 生成匹配日志供人工审核



## no_blank_row.py

由于按照日志进行人工合并时不能将合并后留下的空行删除（否则日志中行号就对不上了），这个py可以将空行删除



## txt_to_json.py

将旧Organization的txt词表变为json输出



## json_cross-compare_delete.py

将旧词表中有的项删除，同义词项之后加ID

+ 如果某一实体在旧词表中有，其在新词表中同义词后会加上ID
+ 可以忽略大小写匹配
+ 可以识别介词位置并通过穷举匹配同义词



## adder.py

将每一行后面加上 ‘**’





### 按照本README的顺序是执行代码的正确顺序，data是示例数据