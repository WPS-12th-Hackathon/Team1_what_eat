from django.contrib import admin
from django.urls import path, include
from .views import sign_up, index, log_in, log_out, naver_login

urlpatterns = [
    path('', index, name='index'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('members/naver-login/', naver_login, name='naver-login'),
]
