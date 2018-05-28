from django.urls import path

from .handlers import AuthenticationHandler, uploadEntryHandler, sendEntryHandler, likeHandler
app_name = 'starpick'

urlpatterns = [
    path('register', AuthenticationHandler.register, name='register'),
    path('login', AuthenticationHandler.login, name="login"),

    path('upload_entry', uploadEntryHandler.uploadEntry, name="upload_entry"),
    path('upload_pick', uploadEntryHandler.uploadPick, name="upload_pick"),

    path('get_pick', sendEntryHandler.sendPick, name="send_pick"),
    path('get_entry', sendEntryHandler.sendEntry, name="sendEntry"),
    path('get_tags', sendEntryHandler.sendTags, name="sendTags"),

    path('like', likeHandler.like, name="like"),
    path('unlike', likeHandler.unlike, name="unlike"),
    path('get_likes', likeHandler.getLikeEntries, name="get_likes"),
]