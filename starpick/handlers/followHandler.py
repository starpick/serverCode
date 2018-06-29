from ..models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlerHelp import *

@csrf_exempt
def followUser(request):
    '''用户关注其他用户'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        # get user
        tokenStr = Info['token']
        token = getToken(tokenStr)
        if token == None: return ERR_TOKEN_RES
        user = token.user

        # get follower
        followerId = Info['followerId'] # follower 的 userid
        try:
            follower = User.objects.get(id=followerId)
        except:
            response.content = toJson({success: False, error: 'wrong follower userId'})
            return response
        
        # save follow
        try:
            follow = Follow.objects.get(user=user, follow=follower)
            response.content = toJson({success: True, 'message': "has followed"})
        except:
            follow = Follow(user=user, follow=follower)
            follow.save()
            response.content = toJson({success: True, "message": "follow success"})
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def unFollowUser(request):
    '''用户关注其他用户'''
    Info = getInfo(request)
    response = HttpResponse()
    try:
        # get user
        tokenStr = Info['token']
        token = getToken(tokenStr)
        if token == None: return ERR_TOKEN_RES
        user = token.user

        # get follower
        followerId = Info['followerId'] # follower 的 userid
        try:
            follower = User.objects.get(id=followerId)
        except:
            response.content = toJson({success: False, error: 'wrong follower userId'})
            return response
        
        # delete follow
        try:
            follow = Follow.objects.get(user=user, follow=follower)
            follow.delete()
            response.content = toJson({success: True, 'message': "unfollowed success"})
        except:
            response.content = toJson({success: False, error: "not followed though"})
        return response
    except:
        return SERVER_ERROR_RES

@csrf_exempt
def getFollowings(request):
    '''获取所有关注的对象'''
    info = getInfo(request)
    response = HttpResponse()
    try:
        userId = info['id']
        try:
            user = User.objects.get(id=userId)
        except:
            response.content = toJson({success: False, error: 'invalid id'})
            return response
        follows = user.follows.all()
        length = len(follows)
        followsList = []
        for i in range(0, length):
            followsList.append(userFrom(follows[i].follow))
        response.content = toJson({
            success: True,
            "follows": followsList
        })
        return response
    except:
        return SERVER_ERROR_RES

def getFollowers(request):
    '''获得所有关注自己的用户列表'''
    info = getInfo(request)
    response = HttpResponse()
    try:
        userId = info['id']
        try:
            user = User.objects.get(id=userId)
        except:
            response.content = toJson({success: False, error: 'invalid id'})
            return response
        followers = user.followers.all()
        length = len(followers)
        followerList = []
        for follower in followers:
            followerList.append(userFrom(follower.user))
        response.content = toJson({
            success: True,
            "followers": followerList
        })
        return response
    except:
        return SERVER_ERROR_RES