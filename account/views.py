from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages

class RegisterView(View):
    form_class = UserRegistrationForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'you registered successfully',
                             'success')
            return redirect('home:home')
        # if the data of the form would be invalid(like empty...) form gets
        # new data with messages. we can use that data and render a new page 
        # for showing them to user.
        return render(request, 'account/register.html', {'form': form})
        

