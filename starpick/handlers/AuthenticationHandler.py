from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ..models import User
import json
from django.views.decorators.csrf import csrf_exempt

# response: 
# https://docs.djangoproject.com/zh-hans/2.0/ref/request-response/#django.http.HttpResponse

user_key = 'user'
password_key = 'password'
success = 'success'
error = 'error'

def toJson(dic):
    return json.dumps(dic)

# 处理用户注册
@csrf_exempt
def register(request):
    response = HttpResponse()
    if request.method == 'GET':
        # 提取请求内容
        Info = request.GET
    else:
        Info = request.POST
    # 查看请求内容中是否包括用户名和密码
    if (user_key in Info) and  (password_key in Info):
        username = Info[user_key]
        password = Info[password_key]
    else:
        response.content = toJson({success: False})
        response.status_code = 400
        return response
    # 用户是否已经存在，若存在，拒绝请求
    user = User.objects.filter(user_name=username)
    if (user.exists()):
        response.content = toJson({success: False, error: 'register fail: user exists'})
        return response
    # 创建新用户并保存入数据库
    newUser = User(user_name = username, password = password)
    newUser.save()
    response.content = toJson({success: True})
    return response

# 处理用户登录
@csrf_exempt
def login(request):
    response = HttpResponse()
    if request.method == 'GET':
        Info = request.GET
    else:
        Info = request.POST
    if (user_key in Info) and  (password_key in Info):
        username = Info[user_key]
        password = Info[password_key]
    else:
        response.status_code = 400
        response.content = toJson({success: False, error: 'bad request'})
        return response
    user = User.objects.filter(user_name=username, password=password)
    if user.exists() == False:
        response.content = toJson({
            success: False,
            error: 'login fail: user not exists or password wrong'
        })
        return response
    user = (list(user))[0]
    response.content = toJson({success: True})
    return response
