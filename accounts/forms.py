from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from .models import Profile

import re

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    confirm_email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    
    
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'password1',
            'password2',
            
        ]
        
        
    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        confirm_email = self.cleaned_data['confirm_email']
        if email != confirm_email:
            raise ValidationError("Emails must match!")
            
        return super(UserRegisterForm, self).clean(*args, **kwargs)
        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
    
        
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=140, label='Biography',
                    widget=forms.Textarea(attrs={'rows': 6}), min_length=10)
    dob = forms.DateField(
        label="Date of birth Ex.('2006-10-25', '10/25/2006', '25/10/06')",
        input_formats = ['%Y-%m-%d',      # '2006-10-25'
                         '%m/%d/%Y',      # '10/25/2006'
                         '%d/%m/%y']      # '25/10/06'
    )
    
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'dob']
        
        
    def clean_bio(self, *args, **kwargs):
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise ValidationError("Your bio must be at least 10 characters long!")
        return bio
        
        

    