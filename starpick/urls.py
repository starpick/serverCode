from django.urls import path

from .handlers import AuthenticationHandler, uploadEntryHandler

app_name = 'starpick'

urlpatterns = [
    path('register', AuthenticationHandler.register, name='register'),
    path('login', AuthenticationHandler.login, name="login"),
    path('upload_entry', uploadEntryHandler.uploadEntry, name="upload_entry"),
    path('upload_pick', uploadEntryHandler.uploadPick, name="upload_pick")
]