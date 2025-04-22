from django.db import models

from users.models import User

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, unique=True, **NULLABLE, verbose_name='Slug')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='posts/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')
    view_count = models.IntegerField(default=0, verbose_name='Счетчик просмотров')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
