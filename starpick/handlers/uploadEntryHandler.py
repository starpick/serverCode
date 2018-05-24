from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

def getToken(tokenStr):
    tokens = Token.objects.filter(token = tokenStr)
    if (len(tokens) == 0):
        return None
    return tokens[0]


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
    if (token == None):
        response.content = toJson({success: False, error: 'unauthorized'})
        return response
    user = token.user
    newEntry = Entry(user = user, picture = 'http://127.0.0.1:8000/admin/starpick/entry/', descreption = description)
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
        if (token == None):
            response.content = {success: False, error: 'invalid token'}
            return response
        entry = Entry.objects.get(id=entryId)
        if (token.user.id != entry.user.id):
            response.content = toJson({
                success: False,
                error: 'token and entry are not belong to the same user'})
            return response

        category = Info['category']
        brand = Info['brand']
        idolName = Info['idolName']
        price = Info['price']
        officialLink = Info['officialLink']
        size = Info['size']
        pic = 'https://github.com/starpi'
        pick = Pick(entry=entry, category=category, brand=brand, idolName=idolName,
            price=price, officialLink=officialLink, size=size, pic=pic)
        pick.save()

        tagX = Info['tagX']
        tagY = Info['tagY']
        tagContent = Info['tagContent']
        tag = Tag(entry=entry, pick=pick, x=tagX, y=tagY, content=tagContent)
        tag.save()

        response.content = toJson({success: True})
        return response
    except:
        response.content = toJson({
            success: False,
            error: 'server error'
        })
        response.status_code = 500
        return response