from django.urls import path

from .handlers import AuthenticationHandler, uploadEntryHandler, sendEntryHandler, likeHandler, followHandler, commentHandler, tagHash, DissHandler, userHandler
app_name = 'starpick'

urlpatterns = [
    path('register', AuthenticationHandler.register, name='register'),
    path('login', AuthenticationHandler.login, name="login"),
    path('get_user', userHandler.getUser, name='getUser'),

    path('upload_entry', uploadEntryHandler.uploadEntry, name="upload_entry"),
    path('upload_pick', uploadEntryHandler.uploadPick, name="upload_pick"),

    path('upload_hashtag', tagHash.setTag, name="upload_hashtag"),
    path('get_entrys_by_hash', tagHash.getEntrysByHash, name='getEntrysByHash'),

    path('get_pick', sendEntryHandler.sendPick, name="send_pick"),
    path('get_entry', sendEntryHandler.sendEntry, name="sendEntry"),
    path('get_tags', sendEntryHandler.sendTags, name="sendTags"),
    path('get_user_entries', sendEntryHandler.sendUserEntry, name="sendTags"),
    path('get_entry_by_likeN', sendEntryHandler.getEntryByLikes, name='getEntryByLikes'),

    path('like', likeHandler.like, name="like"),
    path('unlike', likeHandler.unlike, name="unlike"),
    path('get_likes', likeHandler.sendLikedEntry, name="get_likes"),
    path('query_like', likeHandler.queryLike, name="query_like"),

    path('diss', DissHandler.diss, name="diss"),
    path('undiss', DissHandler.undiss, name="undiss"),
    path('get_disses', DissHandler.sendDissedEntry, name="get_disses"),
    path('query_diss', DissHandler.queryDiss, name="query_diss"),

    path('follow/follow', followHandler.followUser, name="follow"),
    path('follow/unfollow', followHandler.unFollowUser, name="unfollow"),
    path('follow/getfollowings', followHandler.getFollowings, name="getFollowings"),

    path('comment/makecomment', commentHandler.makeComment, name="makecomment"),
    path('comment/getComments', commentHandler.getComments, name="getComments"),
    path('comment/deleteComments', commentHandler.deleteComment, name="deleteComment")
]