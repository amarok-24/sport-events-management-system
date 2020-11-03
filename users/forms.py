from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','first_name','last_name',) # password taken automatically, since it is required!
        # fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name',) # password taken automatically, since it is required!
        # fields = UserChangeForm.Meta.fields 
