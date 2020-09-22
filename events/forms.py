from django import forms
from django.contrib.auth.models import User
from .models import Events ,Book

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        exclude =['user',]

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude =['guest','event']

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
