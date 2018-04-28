from django.http import HttpResponse, HttpResponseRedirect
from ..models import User
import json

# response: 
# https://docs.djangoproject.com/zh-hans/2.0/ref/request-response/#django.http.HttpResponse

user_key = 'user'
password_key = 'password'

# 处理用户注册
def register(request):
    if request.method == 'GET':
        # 提取请求内容
        getInfo = request.GET
        # 查看请求内容中是否包括用户名和密码
        if (user_key in getInfo) and  (password_key in getInfo):
            username = request.GET[user_key]
            password = request.GET[password_key]
        else:
            return HttpResponse('register fail', content_type="text/plain")
        # 用户是否已经存在，若存在，拒绝请求
        user = User.objects.filter(user_name=username)
        if (user.exists()):
            return HttpResponse('register fail: user exists', content_type="text/plain")
        # 创建新用户并保存入数据库
        newUser = User(user_name = username, password = password)
        newUser.save()
        return HttpResponse('register', content_type="text/plain")
    return HttpResponse('info', content_type="application/json")

# 处理用户登录
def login(request):
    if request.method == 'GET':
        getInfo = request.GET
        if (user_key in getInfo) and  (password_key in getInfo):
            username = request.GET[user_key]
            password = request.GET[password_key]
        else:
            return HttpResponse('login fail', content_type="text/plain")
        user = User.objects.filter(user_name=username, password=password)
        if user.exists() == False:
            return HttpResponse('login fail: user not exists', content_type="text/plain")
        user = (list(user))[0]
        print(user.user_name)
        print(user.password)
        return HttpResponse('login success', content_type="text/plain")