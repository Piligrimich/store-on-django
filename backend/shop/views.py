from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth import logout, login as login_user

from cart.forms import CartAddProductForm

from .models import *
from .forms import LoginUserForm, RegisterUserForm, AddComment
from .tasks import send_email_customer


class ProductList(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    extra_context = {'title': 'Каталог'}
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(available=True)


def show_category(request, cat_slug):
    products = Product.objects.filter(category__slug=cat_slug)
    if len(products) == 0:
        return HttpResponse(f'<h1>Список пуст</h1>')
    context = {
        'title': products.first().category.name,
        'products': products,
        'cat_selected': cat_slug,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart_product_form = CartAddProductForm()
    comments = CommentForProduct.objects.filter(product=product)
    form_for_comment = AddComment()
    context = {
        'title': product.name,
        'product': product,
        'cart_product_form': cart_product_form,
        'cat_selected': product.category.slug,
        'comments': comments,
        'form_for_comment': form_for_comment,
    }
    return render(request, 'shop/detail_product.html', context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Вход'}

    def get_success_url(self):
        return reverse_lazy('shop:home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        login_user(self.request, user)
        send_email_customer.delay(user=form.cleaned_data)
        return redirect('shop:home')


def logout_user(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])


def cart_pay(request):
    context = {
        'title': 'Оформление заказа',
    }
    return render(request, 'shop/cart_pay.html', context)


def add_comment_for_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = AddComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.save()
            return redirect(request.META['HTTP_REFERER'])


def delete_comment(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(CommentForProduct, id=comment_id)
        comment.delete()
        return redirect(request.META['HTTP_REFERER'])


def change_comment(request, comment_id):
    comment = get_object_or_404(CommentForProduct, id=comment_id)
    product = get_object_or_404(Product, id=comment.product.id, available=True)

    if request.method == 'GET':
        form_for_comment = AddComment(instance=comment)
        cart_product_form = CartAddProductForm()
        comments = CommentForProduct.objects.filter(product=product)

        context = {
            'title': product.name,
            'product': product,
            'cart_product_form': cart_product_form,
            'cat_selected': product.category.slug,
            'comments': comments,
            'form_for_comment': form_for_comment,
            'comment_id': comment.id,
        }

        return render(request, 'shop/detail_product.html', context)

    if request.method == 'POST':
        form = AddComment(request.POST, instance=comment)
        product = get_object_or_404(Product, id=comment.product.id, available=True)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.save()
            return redirect('shop:product', product_slug=comment.product.slug)
