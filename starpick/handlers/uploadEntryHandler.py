from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *


@csrf_exempt
def uploadEntry(request):
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST

    if (token_key in Info) and (picture_key in Info) and (description_key in Info):
        tokenStr = Info[token_key]
        picture = Info[picture_key]
        description = Info[description_key]
    else:
        response.content = toJson({success: False, error: 'lack of information'})
        return response
    # token 认证
    token = getToken(tokenStr)
    if (token == None): return UNAUTHORIZE_RES
    user = token.user
    newEntry = Entry(user = user, picture = picture, descreption = description)
    newEntry.save()
    response.content = toJson({
        success: True,
        "entryId": newEntry.id
    })
    return response

@csrf_exempt
def uploadPick(request):
    response = HttpResponse()
    if request.method == 'GET': Info = request.GET
    else: Info = request.POST
    try:
        tokenStr = Info[token_key]
        entryId = Info['entryId']

        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        entry = Entry.objects.get(id=entryId)
        if (token.user.id != entry.user.id): return TOKEN_ENTRY_ERR_RES

        if 'category' in Info: category = Info['category']
        else: category = 'none'

        if 'brand' in Info : brand = Info['brand']
        else: brand = 'none'

        if 'idolName' in Info: idolName = Info['idolName']
        else: idolName = 'none'
        
        if 'price' in Info: price = Info['price']
        else: price = '0'
        
        if 'officialLink' in Info: officialLink = Info['officialLink']
        else: officialLink = 'http://none/none'
        
        if 'size' in Info: size = Info['size']
        else: size = '0'
        
        if 'pic' in Info: pic = Info['pic']
        else: pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXF-eeBt3oEZ0oEUbIM0DfzhLz_WODr-NTh4U2mpod2kleXq6D'

        pick = Pick(entry=entry, category=category, brand=brand, idolName=idolName,
            price=price, officialLink=officialLink, size=size, pic=pic)
        pick.save()

        tagX = Info['tagX']
        tagY = Info['tagY']
        tagContent = Info['tagContent']
        tag = Tag(entry=entry, pick=pick, x=tagX, y=tagY, content=tagContent)
        tag.save()

        response.content = toJson({
            success: True,
            'pickId': pick.id,
            'tagId': tag.id
        })
        return response
    except:
        return SERVER_ERROR_RES
