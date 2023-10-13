from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'your email'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'your password'}))
    password_conf = forms.CharField(label='confirm password',
                                    widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                      'placeholder':'your password'}))
    
    
    # validating form data, after we finished our work we have to return the variable
    # that we used(validated).
    def clean_email(self):
        # we must return the email.
        email = self.cleaned_data['email']
        # using exist is more efficent and fatser. we can use below code without using 
        # exists() method but it is not efficent.
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email
    
    def clean_username(self):
        # we have to return the username
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username already exists')
        return username
    
    def clean(self):
        # No need to return a value.
        # get clean data in below manner:
        clean_data = super().clean()
        # we have to use .get() for getting data because it's possible that user did not
        # send any of them. if user did not send a value of form .get() will return None.
        password = clean_data.get('password')
        password_conf = clean_data.get('password_conf')
        if password and password_conf and password != password_conf:
            raise ValidationError('passwords must match.')

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    # Extra fields other than Profile model.
    # We want to edit email field of the User model.
    email = forms.EmailField()
    
    class Meta:
        model = Profile
        fields = ('age', 'bio',)
