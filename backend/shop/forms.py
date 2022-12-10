from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from . models import CommentForProduct


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddComment(ModelForm):

    class Meta:
        model = CommentForProduct
        fields = ['text',]

        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 2,
                                          'placeholder': 'Текст комментари'
                                          }),
        }
