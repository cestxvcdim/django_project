from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone_number = models.CharField(max_length=20, unique=True, **NULLABLE, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Фото профиля')
    country = models.CharField(max_length=50, **NULLABLE, verbose_name='Страна')

    token = models.CharField(max_length=100, **NULLABLE, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []