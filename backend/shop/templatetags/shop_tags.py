from django import template
from shop.models import *


register = template.Library()


@register.inclusion_tag('shop/shop_menu_categories.html')
def show_categories(sort=None, cat_selected=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}
