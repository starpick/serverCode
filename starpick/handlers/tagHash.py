from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def setTag(request):
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST
    try:
        tagName = Info['hashName']
        entryId = Info['entryId']
        entry = Entry.objects.get(id=entryId)
        hashTag = TagHash(entry=entry, hashName=tagName)
        hashTag.save()
        response.content = toJson({
            success: True,
            'tagName': tagName
        })
        return response
    except:
        return SERVER_ERROR_RES

# def getHashTags(request):
#     response = HttpResponse()
#     if request.method == 'GET': Info = request.GET
#     else: Info = request.POST
#     try:
#         entryId = Info['entryId']
#         entry = Entry.objects.get(id=entryId)

@csrf_exempt
def getEntrysByHash(request):
    print('getEntrysByHash')
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST

    try:
        hashName = Info['hashName']
        print(hashName)
        hashTags = TagHash.objects.filter(hashName=hashName)
        print(hashTags)
        lists = []
        print(hashTags)
        for i in range(0, len(hashTags)):
            hashTag = hashTags[i]
            entry = hashTag.entry
            entryInfo = entryForm(entry)
            pickList = []
            for pick in entry.picks.all():
                pickList.append(getPick(pick))
            entryInfo['picks'] = pickList
            lists.append(entryInfo)
        response.content = toJson({
            success: True,
            'entries': lists
        })
        return response
    except:
        return SERVER_ERROR_RES
        