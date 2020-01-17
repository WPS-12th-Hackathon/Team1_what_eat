from django.contrib import admin
from django.urls import path, include
from .views import sign_up, index, log_in

urlpatterns = [
    path('', index, name='index'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
]