from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *


def sendLikedEntry(request):
    '''向客户端发送entry'''
    # 给定entryId
    Info = getInfo(request)
    response = HttpResponse()
    try:
        email = Info['user_email']
        try:
            user = User.objects.get(email=email)
        except:
            response.content = toJson({success: False, error: 'invalid user'})
        entrys = 
        response.content = toJson({
            success: True,
            "entry": getEntry(entryId)
        })
        return response
    except:
        return SERVER_ERROR_RES