import upyun

# 新建又拍云实例    空间名称       操作员                 密码
up = upyun.UpYun('tianshangxing', 'xing', 'tTj32mkTmBeMoM9pUYo9AG5tuNx5f7fF')

# 上传文件
# up.put('/upyun_test.txt', 'hello\n你好')

# 文件流操作(节省内存)
# with open('./md.png', 'rb') as f:
#     # 上传操作
#     res = up.put('/upyun_test.png', f, checksum=True)

# 创建文件夹
# up.mkdir('/upyun_test/')

# 移动文件
# up.move('/upyun_test.png', '/upyun_test/upyun_test.png')

# 复制文件
# up.copy('/upyun_test.txt', '/upyun_test/upyun_test.txt')

# 断点续传
# with open('D:/12594/Music/MV/米津玄師/米津玄師 - LOSER.mp4', 'rb') as f:
#     res = up.put('/upyun_test/米津玄師 - LOSER.mp4', f, checksum=True, need_resume=True)

# 下载文件
# res = up.get('/upyun_test/upyun_test.txt')
# print(res)

# 删除文件
# res = up.delete('/upyun_test/upyun_test.png')