from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def like(request):
    '''添加用户喜欢'''
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
            entry.likenumber += 1
            entry.save()
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
            entry.likenumber -= 1
            entry.save()
            response.content = toJson({success: True, "message": "unlike success"})
            return response
        except:
            response.content = toJson({success: False, error: "have not been liked"})
            return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def queryLike(request):
    '''给定email和entryId，查询email代表的用户是否喜欢该entry'''
    # 返回 true 或 false
    Info = getInfo(request)
    response = HttpResponse()
    try:
        email = Info['email']
        entryId = Info['entryId']
        try:
            user = User.objects.get(email=email)
            entry = Entry.objects.get(id=entryId)
        except:
            response.content = toJson({success: False, error: 'unvalid user email or entry'})
            return response
        try:
            like = Like.objects.get(user=user, entry=entry)
            response.content = toJson({success: True, "like": True})
        except:
            response.content = toJson({success: True, "like": False})
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def sendLikedEntry(request):
    '''给定email，返回like entry'''
    # 给定 email，返回用户所有喜欢的entry
    Info = getInfo(request)
    response = HttpResponse()
    try:
        email = Info['email']
        print(email)
        try:
            user = User.objects.get(email=email)
        except:
            response.content = toJson({success: False, error: 'invalid user'})
            return response
        likes = user.likes.all()
        entryList = []
        for i in range(0, len(likes)):
            print(likes[i].id)
            entryList.append(getTagAndEntry(likes[i].entry.id))
        response.content = toJson({
            success: True,
            "entry": entryList
        })
        return response
    except:
        return SERVER_ERROR_RES