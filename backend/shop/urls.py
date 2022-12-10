from django.urls import path
from .views import *


app_name = 'shop'
urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('product/<slug:product_slug>/', product_detail, name='product'),
    path('categories/<slug:cat_slug>/', show_category, name='category'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('cartpay/', cart_pay, name='cart_pay'),
    path('add_comment/<int:product_id>/', add_comment_for_product, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('change_comment/<int:comment_id>', change_comment, name='change_comment'),

]
