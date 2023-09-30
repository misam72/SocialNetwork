from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'your password'}))
    
    # validating form data, after we finished our work we have to return the variable
    # that we used(validated).
    def clean_email(self):
        email = self.cleaned_data['email']
        # using exist is more efficent and fatser. we can use below code without using 
        # exists() method but it is not efficent.
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email