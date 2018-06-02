from django.urls import path

from .handlers import AuthenticationHandler, uploadEntryHandler, sendEntryHandler, likeHandler, followHandler, commentHandler
app_name = 'starpick'

urlpatterns = [
    path('register', AuthenticationHandler.register, name='register'),
    path('login', AuthenticationHandler.login, name="login"),

    path('upload_entry', uploadEntryHandler.uploadEntry, name="upload_entry"),
    path('upload_pick', uploadEntryHandler.uploadPick, name="upload_pick"),

    path('get_pick', sendEntryHandler.sendPick, name="send_pick"),
    path('get_entry', sendEntryHandler.sendEntry, name="sendEntry"),
    path('get_tags', sendEntryHandler.sendTags, name="sendTags"),
    path('get_user_entries', sendEntryHandler.sendUserEntry, name="sendTags"),

    path('like', likeHandler.like, name="like"),
    path('unlike', likeHandler.unlike, name="unlike"),
    path('get_likes', likeHandler.sendLikedEntry, name="get_likes"),
    path('query_like', likeHandler.queryLike, name="query_like"),

    path('follow/follow', followHandler.followUser, name="follow"),
    path('follow/unfollow', followHandler.unFollowUser, name="unfollow"),
    path('follow/getfollowings', followHandler.getFollowings, name="getFollowings"),

    path('comment/makecomment', commentHandler.makeComment, name="makecomment"),
    path('comment/getComments', commentHandler.getComments, name="getComments")
]