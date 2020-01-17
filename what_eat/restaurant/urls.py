
from django.urls import path
from .views import view_restaurant, bookmark, bookmark_list, delete_bookmark

app_name = 'restaurant'

urlpatterns = [
    path('restaurant/<int:page>', view_restaurant, name='view_restaurant'),
    path('bookmark/', bookmark, name='bookmark'),
    path('bookmark/list/', bookmark_list, name='bookmark_list'),
    path('<int:pk>/delete_bookmark/', delete_bookmark, name='delete_bookmark')
]
