from django.db import models

from members.views import User


class Restaurant(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=50)
    menu = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    tel = models.CharField(max_length=30)
