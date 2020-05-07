import jwt
import datetime

# 载荷中加入生命周期
playload = {
    # 过期时间
    'exp': int((datetime.datetime.now() + datetime.timedelta(seconds=30)).timestamp()),
    'data': {'uid': 1, 'username': 'test'}
}

# 生成jwt
encode_jwt = jwt.encode({'uid': 2}, 'xing', algorithm='HS256')

# 转码
encode_str = str(encode_jwt, 'utf-8')

# 解密操作
try:
    decode_jwt = jwt.decode(encode_str, 'xing', algorithm='HS256')
except Exception as e:
    print('密钥已经过期')
    pass

print(encode_str)

print(decode_jwt['uid'])