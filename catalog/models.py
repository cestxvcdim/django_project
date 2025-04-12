from django.db import models

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(default=1, verbose_name='Номер версии')
    version_title = models.CharField(max_length=255, verbose_name='Название версии')
    is_actual = models.BooleanField(default=True, verbose_name='Версия актуальна?')

    def __str__(self):
        return f'{self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
