import requests

# 定义要上传的文件   文件名                文件实体
files = {'file': ('1.jpg', open('C:/Users/12594/Pictures/Camera Roll/your_name.png', 'rb'))}

# 发起请求
res = requests.post('http://127.0.0.1:8000/upload/', files=files)

print(res.text)