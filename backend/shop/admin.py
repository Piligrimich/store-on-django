from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_show', 'slug', 'price', 'stock', 'available', 'date_create', 'date_update',)
    list_filter = ('available', 'date_create', 'date_update',)
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = 'Картинка'


admin.site.register(Product, ProductAdmin)


class CommentForProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'date_create',)
    list_filter = ('user', 'product',)
    list_editable = ('text',)


admin.site.register(CommentForProduct, CommentForProductAdmin)
