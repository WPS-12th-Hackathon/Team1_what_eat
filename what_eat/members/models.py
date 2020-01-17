from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField('이름', max_length=100)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
