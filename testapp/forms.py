from django import forms
#from django.contrib.auth.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
'''class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']'''



class SignUpForm(UserCreationForm):
 password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
 password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
 email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
 class Meta:
  model = User
  fields = ['username', 'email', 'password1', 'password2']
  labels = {'email': 'Email'}
  widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}























'''class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username','password','email','first_name','last_name']'''        
