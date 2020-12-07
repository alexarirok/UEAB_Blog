from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from tinymce import TinyMCE

from django.contrib.auth import (
    authenticate,
    get_user_model
    )
User = get_user_model()

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,)
    last_name = forms.CharField(max_length=30, required=True,)
    email = forms.EmailField(max_length=60, help_text='Required. Add valid email Address')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self,).clean(*args, **kwargs)
    
# class UserRegisterForm(forms.ModelForm):
#     email = forms.EmailField(label='Email Address')
#     email2 = forms.EmailField(label='Confirm Address')
#     password = forms.PasswordInput()
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'email2',
#             'password'
#         ]
        
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         email2 = self.cleaned_data.get('email2')
#         if email != email2:
#             raise forms.ValidationError('emails must match')
#         email_qs = User.objects.filter(email=email)
#         if email_qs.exists():
#             raise forms.ValidationError('This email is already being used')
#         return email

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
    
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post')
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'username',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )   
