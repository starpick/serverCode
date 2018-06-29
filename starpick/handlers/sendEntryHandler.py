from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def sendEntry(request):
    '''向客户端发送entry'''
    # 给定entryId
    Info = getInfo(request)
    response = HttpResponse()
    try:
        entryId = Info['entryId']
        response.content = toJson({
            success: True,
            "entry": getEntry(entryId)
        })
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def sendTags(request):
    '''向客户端发送tags'''
    # 给定entryId
    Info = getInfo(request)
    response = HttpResponse()
    try:
        entryId = Info['entryId']
        entry = Entry.objects.get(id=entryId)
        tags = entry.tags.all()
        tagList = []
        length = len(tags)
        for i in range(0, length):
            tagList.append(getTag(tags[i]))
        response.content = toJson({
            success: True,
            "tagLength": length,
            "tags": tagList,
        })
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def sendPick(request):
    # 给定 tagID，查询 pick
    # 使用get方法：http://127.0.0.1:8000/starpick/send_pick?tagId=3
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST
    try:
        pickId = Info['pickId']
        pick = Pick.objects.get(id=pickId)
        
        response.content = toJson({
            success: True,
            "pick": getPick(pick)
        })
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def sendUserEntry(request):
    '''发送用户创建的所有 entry'''
    # 给定 email
    Info = getInfo(request)
    response = HttpResponse()
    try:
        email = Info['email']
        try:
            user = User.objects.get(email=email)
        except:
            response.content = toJson({success: False, error: 'invalid user'})
            return response
        entries = user.entry.all()
        entryList = []
        for i in range(0, len(entries)):
            entryList.append(getTagAndEntry(entries[i].id))
        response.content = toJson({
            success: True,
            "entry": entryList
        })
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def getEntryByLikes(request):
    Info = getInfo(request)
    response = HttpResponse()
    try:
        numLimit = 30
        if 'numLimit' in Info:
            numLimit = int(Info['numLimit'])
        entries = Entry.objects.all().order_by('-likenumber')[0:numLimit]
        entryList = []
        for entry in entries:
            entryList.append(entryForm(entry))
        response.content = toJson({
            success: True,
            'entries': entryList
        })
        return response
    except:
        return SERVER_ERROR_RES