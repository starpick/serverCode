from django.urls import path

from .handlers import AuthenticationHandler

app_name = 'starpick'

urlpatterns = [
    path('register', AuthenticationHandler.register, name='register'),
    path('login', AuthenticationHandler.login, name="login")
]