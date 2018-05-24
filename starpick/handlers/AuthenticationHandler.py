from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from django.core import signing
import hashlib
import time

from ..models import *
from .handlerHelp import *

# response: 
# https://docs.djangoproject.com/zh-hans/2.0/ref/request-response/#django.http.HttpResponse

def create_token(user):
    # 生成token信息
    # 1. 加密头信息
    email = user.email
    user_name = user.user_name
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload = {"email": email, "user_name": user_name, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    tokenStr = "%s.%s.%s" % (header, payload, signature)
    
    # 存储到数据库,若数据库已有token，更新token，否则重新存储一个token
    old_token = user.token.all()
    if (len(old_token) == 0):
        token = Token(token = tokenStr, user = user)
        token.save()
    else:
        old_token[0].token = tokenStr
        old_token[0].save()
    return tokenStr


# 处理用户注册
@csrf_exempt
def register(request):
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST

    if (user_key in Info) and  (password_key in Info) and (email_key in Info):
        username = Info[user_key]
        password = Info[password_key]
        email = Info[email_key]
    else:
        response.content = toJson({success: False, error: 'not enough parameter'})
        response.status_code = 400
        return response
    
    user = User.objects.filter(email = email)
    if user.exists() == True:
        response.content = toJson({
            success: False,
            error: 'The email has been used'
        })
        return response

    # 创建新用户并保存入数据库
    newUser = User(user_name = username, password = makePassword(password), email = email)
    newUser.save()
    token = create_token(newUser)
    response.content = toJson({success: True, "token": token})
    return response


# 处理用户登录
@csrf_exempt
def login(request):
    response = HttpResponse()
    if request.method == 'GET':
        Info = request.GET
    else:
        Info = request.POST
    if (email_key in Info) and  (password_key in Info):
        email = Info[email_key]
        password = Info[password_key]
    else:
        response.status_code = 400
        response.content = toJson({success: False, error: 'bad request'})
        return response

    user = User.objects.filter(email = email)
    if user.exists() == False:
        response.content = toJson({
            success: False,
            error: 'login fail: user not exists or password wrong'
        })
        return response
    user = (list(user))[0]
    
    if (user.id): print('user:' + str(user.id))
    else: print('not exsit')
    if checkPassword(password, user.password) == False:
        response.content = toJson({
            success: False,
            error: 'login fail: wrong password'
        })
        return response
    token = create_token(user)
    response.content = toJson({success: True, "token": token})
    return response
