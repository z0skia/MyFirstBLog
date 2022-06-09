#Blog
from django import forms
from .models import Post
from blog import models
#USER SYSTEM
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User





class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'post_body', 'image_up')
   
#USER SYSTEM

class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username', 'email', 'password1', 'password2')
        help_texts={hlp:"" for hlp in fields}
    