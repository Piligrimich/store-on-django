from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image


class Product(models.Model):
    name = models.CharField('Название', max_length=255, db_index=True)
    slug = models.SlugField('URL', unique=True, db_index=True)
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField('Описание', blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата изменения', auto_now=True)
    category = models.ForeignKey('Category', verbose_name='Каткгории', on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Остаток на складе')
    available = models.BooleanField('Доступен', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, db_index=True)
    slug = models.SlugField('URL', unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class CommentForProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'