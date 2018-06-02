from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def makeComment(request):
    '''用户评论'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        tokenStr = Info['token']
        entryId = Info['entryId']
        content = Info['content']
        token = getToken(tokenStr)
        if (token == None): return UNAUTHORIZE_RES
        user = token.user 
        entry = Entry.objects.get(id=entryId)
        comment = Comment(entry=entry, user=user, content=content)
        comment.save()
        entry.commentnumber += 1
        entry.save()
        response.content = toJson({success: True, 'message': 'comment success'})
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def getComments(request):
    Info = getInfo(request)
    response = HttpResponse()
    try:
        entryId = Info['entryId']
        entry = Entry.objects.get(id=entryId)
        comments = entry.comments.all()
        commentList = []
        length = len(comments)
        for i in range(0, length):
            user = comments[i].user
            comment = {
                "userid": user.id,
                "username": user.user_name,
                "content": comments[i].content
            }
            commentList.append(comment)
        response.content = toJson({
            success: True,
            "comments": commentList
        })
        return response
    except:
        return SERVER_ERROR_RES