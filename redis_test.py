# 导包
import redis

# 定义ip和端口
host = 'localhost'
port = 6379

# 建立链接
r = redis.Redis(host=host, port=port)

# # 赋值
# r.set('test', 'test')

# # 取值 二进制 速度快
# code = r.get('test')

# # 转码
# code = code.decode('utf8')

# print(code)

# 列表操作
# r.lpush("xing",1)

# 过期时间 单位是秒
# r.expire("xing",30)

# 打印过期时间
print(r.ttl('xing'))

# 打印列表长度
print(r.llen("xing"))

if r.llen("xing") > 5:
	print('您的账号被锁定了')
