from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

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


def sendPick(request):
    # 给定 tagID，查询 pick
    # 使用get方法：http://127.0.0.1:8000/starpick/send_pick?tagId=3
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST
    try:
        tagId = Info['tagId']
        print(tagId)
        tag = Tag.objects.get(id=tagId)
        pick = tag.pick
        
        response.content = toJson({
            success: True,
            "pick": getPick(pick)
        })
        return response
    except:
        return SERVER_ERROR_RES