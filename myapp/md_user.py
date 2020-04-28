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
		img_size = (120, 50)
		# 定义图片对象
		image = Image.new('RGB', img_size, 'white')
		# 定义画笔
		draw = ImageDraw.Draw(image, 'RGB')
		# 定义内容
		source = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
			draw.text((10 + 30 * i, 20), random_str, text_color)
		
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