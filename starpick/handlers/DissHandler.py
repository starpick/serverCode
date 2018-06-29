from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def diss(request):
    '''添加用户diss'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        tokenStr = Info['token']
        entryId = Info['entryId']
        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user 
        entry = Entry.objects.get(id=entryId)
        # 先检测是否已经diss,代价是否会太高？
        try:
            diss = Diss.objects.get(user=user, entry=entry)
            response.content = toJson({success: False, error: 'has been dissed'})
            return response
        except:
            diss = Diss(user=user, entry=entry)
            diss.save()
            entry.dissnumber += 1
            entry.save()
            response.content = toJson({success: True})
            return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def undiss(request):
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
            diss = Diss.objects.get(user=user, entry=entry)
            diss.delete()
            entry.dissnumber -= 1
            entry.save()
            response.content = toJson({success: True, "message": "undiss success"})
            return response
        except:
            response.content = toJson({success: False, error: "have not been dissed"})
            return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def queryDiss(request):
    '''给定email和entryId，查询email代表的用户是否diss该entry'''
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
            diss = Diss.objects.get(user=user, entry=entry)
            response.content = toJson({success: True, "diss": True})
        except:
            response.content = toJson({success: True, "diss": False})
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def sendDissedEntry(request):
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
        diss = user.diss.all()
        entryList = []
        for i in range(0, len(diss)):
            print(diss[i].id)
            entryList.append(getTagAndEntry(diss[i].entry.id))
        response.content = toJson({
            success: True,
            "entry": entryList
        })
        return response
    except:
        return SERVER_ERROR_RES