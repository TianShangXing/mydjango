import requests

# 定义要上传的文件   文件名                文件实体
files = {'file': ('人物男头01.jpg', open('D:/Download/网盘下载文件/人物男头01.jpg', 'rb'))}

# 发起请求
res = requests.post('http://127.0.0.1:8000/uploadup/', files=files)

print(res.text)