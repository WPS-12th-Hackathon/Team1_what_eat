
from django.urls import path
from .views import view_restaurant, bookmark
app_name = 'restaurant'

urlpatterns = [
    path('restaurant/', view_restaurant, name='view_restaurant'),
    path('bookmark/', bookmark, name='bookmark')
]
