# from mpython import *
import binascii

info = '深圳市第二高级中学'

# 转码
loc_info = binascii.hexlify(info.encode('utf-8'))
print("转码后:" + str(loc_info), "\ninfo:", info)
print('loc_info:', type(loc_info))

# new_info = str(loc_info).replace("b", "").replace("'", "")
new_info = loc_info.decode()
print('str格式', new_info)

print('\n\n\n')

# 解码
bin_info = binascii.unhexlify(loc_info)
print('解码info', bin_info)

nb_info = bin_info.decode()
print(nb_info)




# output
# 转码后:b'e6b7b1e59cb3e5b882e7acace4ba8ce9ab98e7baa7e4b8ade5ada6' 
# info: 深圳市第二高级中学
# loc_info: <class 'bytes'>
# str格式 e6b7b1e59cb3e5b882e7acace4ba8ce9ab98e7baa7e4b8ade5ada6



# 解码info b'\xe6\xb7\xb1\xe5\x9c\xb3\xe5\xb8\x82\xe7\xac\xac\xe4\xba\x8c\xe9\xab\x98\xe7\xba\xa7\xe4\xb8\xad\xe5\xad\xa6'                                                                                                          ad\xa6'
# 深圳市第二高级中学