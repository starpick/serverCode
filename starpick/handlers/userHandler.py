from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def getUser(request):
    '''get user info'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        userId = Info['userId']
        user = User.objects.get(id=userId)
        response.content = toJson(userFrom(user))
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def editUserInfo(request):
    '''edit the user's info, can edit username, headurl'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        if 'token' not in Info: return UNAUTHORIZE_RES
        tokenStr = Info['token']
        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user
        if 'username' in Info:
            user.user_name = Info['username']
        if 'header' in Info:
            user.header = Info['header']
        user.save()
        response.content = toJson({
            success: True,
            'user': userFrom(user)
        })
        return response
    except:
        return SERVER_ERROR_RES