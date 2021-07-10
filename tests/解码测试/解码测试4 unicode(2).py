str = '深圳市第二高级中学'
uni = str.encode('unicode-escape').decode()
print(uni)
print(type(uni))