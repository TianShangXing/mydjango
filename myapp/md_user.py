from django.shortcuts import render,redirect
# 导包
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# 导入类视图
from django.views import View

# 导入表
from myapp.models import User

import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView

# 导入加密库
import hashlib
# 导入图片库
# 绘画库
from PIL import ImageDraw
# 字体库
from PIL import ImageFont
# 图片库
from PIL import Image
# 随机库
import random
# 文件流
import io

# 发请求库
import requests

# 导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

# 导入原生sql模块
from django.db import connection

import jwt

# 导入时间模块
import time

# 导入公共目录变量
from mydjango.settings import BASE_DIR

# 导包
from django.db.models import Q,F

# 导入dwebsocket的库
from dwebsocket.decorators import accept_websocket
import uuid

# 导入redis数据库
import redis

# 定义ip和端口
host = 'localhost'
port = 6379

# 建立链接
r = redis.Redis(host=host, port=port)

# 又拍云上传
import upyun
# 定义文件上传类
class UploadUp(APIView):
	def post(self,request):
		# 获取文件
		file = request.FILES.get('file')
		# 新建又拍云实例    空间名称       操作员                 密码
		up = upyun.UpYun('tianshangxing', 'xing', 'tTj32mkTmBeMoM9pUYo9AG5tuNx5f7fF')
		# 声明头部信息
		headers = {'x-gmkerl-rotate': 'auto'}

		# 上传图片
		for chunk in file.chunks():
			# 又拍云路径
			res = up.put('test.jpg', chunk, checksum=True, headers=headers)

		return Response({'filename': file.name})

# 七牛云token
from qiniu import Auth

class QiNiu(APIView):
	def get(self, request):
		# 声明认证对象            AK                                        SK
		q = Auth('gne8IIvxIQPLlv5U6PoSHWi5RKbRWObzcfPU-zse', 'SePCg8HiTpN5_ugZ9uYhN0BxWWXzMWPC0KJ5GdcD')
		# 获取token           空间名称
		token = q.upload_token('xing3')
		
		return Response({'token': token})

# 文件上传通用类
class UploadFile(APIView):
	# get 超出文件限制报错
	def post(self, request):
		# 接收参数
		myfile = request.FILES.get('file')

		uid = request.POST.get('uid', None)

		# 建立文件流对象 定义写文件路径
		f = open(os.path.join(UPLOAD_ROOT, '', myfile.name.replace('"', '')), 'wb')

		# 写入
		for chunk in myfile.chunks():
			f.write(chunk)
		f.close()

		# 打开图片
		im = Image.open(myfile)

        # 生成画笔对象
		draw = ImageDraw.Draw(im)

        # 设置字体
		my_font = ImageFont.truetype('c:\\Windows\\Fonts\\BAUHS93.TTF', size=50)

		# 修改图片
		draw.text((500, 500), 'Xing', font=my_font ,fill=(76, 234, 124, 180))

		# 定义存储路径
		storagepath='./static/upload/'+myfile.name

		im.save(storagepath)

		# 修改头像地址
		user = User.objects.get(id=int(uid))
		user.img = myfile.name.replace('"', '')
		user.save()

		return Response({'filename': myfile.name.replace('"', '')})

# 钉钉回调方法
import hmac
import base64
from hashlib import sha256
import urllib

def ding_back(request):
    #获取code
    code = request.GET.get("code")

    t = time.time()

    # 时间戳
    timestamp = str((int(round(t * 1000))))
    appSecret ='fp3nkGoIhS2Mi9EdVql_nKXg6Y0-HSGp-2F_p7IAv_Quc56yhhrinpqbcQRg3RqF'

    # 构造签名
    signature = base64.b64encode(hmac.new(appSecret.encode('utf-8'),timestamp.encode('utf-8'), digestmod=sha256).digest())

    # 请求接口，换取钉钉用户名
    payload = {'tmp_auth_code':code}
    headers = {'Content-Type': 'application/json'}
    res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature='+urllib.parse.quote(signature.decode("utf-8"))+"&timestamp="+timestamp+"&accessKey=dingoahmelrgy51wltnjzs",data=json.dumps(payload),headers=headers)

    res_dict = json.loads(res.text)
    print(res_dict)
    # return HttpResponse(res.text)

	# 判断是否为第一次钉钉登录
    user = User.objects.filter(username=str(res_dict['user_info']['nick'])).first()

    ding_id = ''
    user_id = ''

    if user:
        # 代表曾经用过钉钉登录
        ding_id = user.username
        user_id = user.id

    else:
        # 代表首次登录，入库
        user = User(username=str(res_dict['user_info']['nick']), password='')
        # 保存入库
        user.save()
        
        # 查询用户id
        user = User.objects.filter(username=str(res_dict['user_info']['nick'])).first()
        ding_id = str(res_dict['user_info']['nick'])
        user_id = user.id
    # 进行跳转
    return redirect('http://localhost:8080?ding_id=' + str(ding_id) + '&uid=' + str(user_id))


# 新浪微博回调方法
def wb_back(request):
	# 接收参数
	code = request.GET.get('code', None)

	# 定义token接口地址
	url = 'https://api.weibo.com/oauth2/access_token'

	# 定义参数
	re = requests.post(url, data={
		'client_id': 1484610767,
		'client_secret': 'e61c56200479acd83075a88fb1ab4a87',
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': 'http://127.0.0.1:8000/md_admin/weibo'
	})

	# 换取新浪微博用户昵称
	res = requests.get('https://api.weibo.com/2/users/show.json', params={'access_token': re.json()['access_token'], 'uid': re.json()['uid']})

	sina_id = ''
	user_id = ''

	# 判断是否用新浪微博登陆过
	user = User.objects.filter(username=str(res.json()['name'])).first()

	if user:
		# 代表曾经用该账号登录过
		sina_id = user.username
		user_id = user.id

	else:
		# 首次登录，入库
		user = User(username=str(res.json()['name']), password=str(res.json()['id']))
		user.save()

		user = User.objects.filter(username=str(res.json()['name'])).first()

		sina_id = user.username
		user_id = user.id

	# 重定向
	return redirect('http://localhost:8080/?sina_id='+ str(sina_id) + '&uid=' + str(user_id))

# 自定义图片验证码
class MyCode(View):
	# 定义RGB随机颜色
	def get_random_color(self):
		R = random.randrange(255)
		G = random.randrange(255)
		B = random.randrange(255)

		return(R, G, B)

	# 定义图片视图
	def get(self, request):
		# 画布
		img_size = (130, 60)
		# 定义图片对象
		image = Image.new('RGB', img_size, '#FFFFE0')
		# 定义画笔
		draw = ImageDraw.Draw(image, 'RGB')
		# 定义内容
		source = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		# 定义字体
		my_font = ImageFont.truetype(font="c:\\Windows\\Fonts\\comic.ttf", size=25)
		# 接收容器
		code_str = ''
		# 进入循环绘制
		for i in range(4):
			# 获取字体颜色
			text_color = self.get_random_color()
			# 获取随机下标
			tmp_num = random.randrange(len(source))
			# 随机字符串
			random_str = source[tmp_num]
			# 装入容器中
			code_str += random_str
			# 绘制字符串   坐标(x, y)     随机字符串   字体颜色
			draw.text((10 + 30 * i, 10), random_str, text_color, font=my_font)
		
		# 获取缓冲区
		buf = io.BytesIO()
		# 将临时图片保存到缓冲区
		image.save(buf, 'png')
		# 保存随机码
		r.set('code', code_str)

		#保存session
		request.session['code'] = code_str

		print(r.get('code'))

		return HttpResponse(buf.getvalue(), 'image/png')



# 登录接口
class Login(APIView):
	def get(self, request):
		# 接收参数
		username = request.GET.get('username', None)
		password = request.GET.get('password', None)
		code = request.GET.get('code',None)

		# 比对验证码
		redis_code = r.get("code")
		# 转码 str(redis_code,'utf-8')
		redis_code = redis_code.decode("utf-8")

		# 从session取值
		session_code = request.session.get('code',None)

		print(session_code)

		if code != redis_code:
			return Response({'code':403,'message':'您输入的验证码有误'})

		# 查询数据 .get：查询不到报错 .filter：全表搜索，性能较慢
		user = User.objects.filter(username=username, password=make_password(password)).first()

		if user:
			return Response({'code': 200, 'message': '登陆成功', 'uid': user.id, 'username': user.username})

		else:
			return Response({'code':403, 'message': '用户名或密码错误'})

# md5加密方法
def make_password(mypass):

	# 生成md5对象
	md5 = hashlib.md5()

	# 转码操作
	mypass_utf8 = str(mypass).encode(encoding="utf-8")

	# 加密操作
	md5.update(mypass_utf8)

	# 返回密文
	return md5.hexdigest()

# 注册接口
class Register(APIView):

	def get(self,request):

		# 接收参数
		username = request.GET.get('username',None)
		password = request.GET.get('password',None)

		# 排重操作
		user = User.objects.filter(username=username).first()

		if user:
			return Response({'code':403,'message':'该用户名已经存在'})

		# 入库
		user = User(username=username,password=make_password(password))

		# 保存结果
		user.save()

		return Response({'code':200,'message':'恭喜注册成功'})

	def post(self,request):

		# 接收参数
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		# 排重操作
		user = User.objects.filter(username=username).first()

		if user:
			return Response({'code':403,'message':'该用户名已经存在'})

		# 入库
		user = User(username=username,password=make_password(password))

		# 保存结果
		user.save()

		return Response({'code':200,'message':'恭喜注册成功'})