from django import forms

from .models import CustomUser
class UsersForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    region = forms.CharField(max_length=100,  required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    
    
class LoginForm(forms.Form):
    email = UsersForm.base_fields['email']
    password = UsersForm.base_fields['password']
    
    
    
