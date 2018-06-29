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