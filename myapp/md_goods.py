from django.shortcuts import render,redirect
#导包
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
#导入类视图
from django.views import View

import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
#导入加密库
import hashlib
#导入图片库
#绘画库
from PIL import ImageDraw
#字体库
from PIL import ImageFont
#图片库
from PIL import Image
#随机库
import random
#文件流
import io

import requests

#导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

#导入原生sql模块
from django.db import connection

import jwt

#导入redis数据库
import redis

#导入时间模块
import time

#导入公共目录变量
from mydjango.settings import BASE_DIR

#导包
from django.db.models import Q,F

#导入dwebsocket的库
from dwebsocket.decorators import accept_websocket
import uuid

from myapp.models import User, Carousel, Goods, Category

#导入序列化对象
from myapp.myser import CarouselSer, CategorySer, GoodsSer

#定义地址和端口
host = '127.0.0.1'
port = 6379

#建立redis连接
r = redis.Redis(host=host,port=port)

# 商品信息接口
class GoodInfo(APIView):
    def get(self, request):
        id = request.GET.get('id', None)

        # 查询数据
        good = Goods.objects.get(id=id)

        # 序列化操作
        good_ser = GoodsSer(good)

        return Response(good_ser.data)

# 商品列表页
class GoodsList(APIView):
    def get(self, request):
        # 当前页
        page = request.GET.get('page', 1)

        # 一页展示个数
        size = request.GET.get('size', 1)

        # 计算从哪切
        data_start = (int(page) - 1) * int(size)

        # 计算切到哪
        data_end = int(page) * int(size)

        # 查询
        goods = Goods.objects.all()[data_start: data_end]

        # 查询所有商品个数
        count = Goods.objects.count()

        # 序列化
        goods_ser = GoodsSer(goods, many=True)

        return Response({'data': goods_ser.data, 'total': count})


# 商品分类接口
class CategoryList(APIView):
    def get(self, request):
        category = Category.objects.all()

        category_ser = CategorySer(category, many=True)

        return Response(category_ser.data)

# 商品入库接口
class InsertGoods(APIView):
    def get(self, request):
        # 接收参数
        name = request.GET.get('name', None)

        price = request.GET.get('price', None)

        params = request.GET.get('params', None)

        cid = request.GET.get('cid', None)

        # 排重操作
        goods = Goods.objects.filter(name=name).first()

        if goods:
            return Response({'code': 403, 'message': '您已经添加过了该商品'})

        # 入库
        goods = Goods(name=name, price=price, params=params, cid=cid)

        goods.save()

        return Response({'code': '200', 'message': '添加商品成功'})
