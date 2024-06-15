from django.contrib.auth.models import User
from django import forms


class AddRecordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']