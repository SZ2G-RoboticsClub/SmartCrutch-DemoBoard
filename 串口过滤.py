#coding=utf-8
# 声明两个列表变量
list1 = ['PHP', 'JavaScript']
list2 = ['JavaScript是客户端脚本语言',
    'PHP是服务器端脚本语言',
     'Java是一种编程语言',
    'Kotlin是一种静态编程语言']
 
# 根据第一个列表过滤第二个列表
filter_data = [x for x in list2 for y in list1 if y in x ]
 
# 在过滤前和过滤后打印列表数据
print("第一个列表的内容:", list1)
print("第二个列表的内容:", list2)
print("过滤后的第二个列表的内容:", filter_data)