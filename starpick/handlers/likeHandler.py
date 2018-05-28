from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def like(request):
    Info = getInfo(request)
    response = HttpResponse()
    try:
        tokenStr = Info['token']
        entryId = Info['entryId']

        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user 
        entry = Entry.objects.get(id=entryId)
        # 先检测是否已经like,代价是否会太高？
        try:
            likes = Like.objects.get(user=user, entry=entry)
            response.content = toJson({success: False, error: 'has been liked'})
            return response
        except:
            like = Like(user=user, entry=entry)
            like.save()
            response.content = toJson({success: True})
            return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def unlike(request):
    '''取消喜欢'''
    # 和 like 逻辑相似,是否合并？
    Info = getInfo(request)
    response = HttpResponse()
    try:
        tokenStr = Info['token']
        entryId = Info['entryId']
        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user 
        entry = Entry.objects.get(id=entryId)
        # 先检测是否已经like,代价是否会太高？
        try:
            like = Like.objects.get(user=user, entry=entry)
            like.delete()
            response.content = toJson({success: True, "message": "unlike success"})
            return response
        except:
            response.content = toJson({success: False, error: "have not been liked"})
            return response
    except:
        return SERVER_ERROR_RES


@csrf_exempt
def getLikeEntries(request):
    Info = getInfo(request)
    response = HttpResponse()
    try:
        tokenStr = Info['token']
        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user
        likes = user.likes.all()
        response.content = toJson({success: True, "length": len(likes)})
        return response
    except:
        return SERVER_ERROR_RES