from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    # Class variables for clean code purpose.
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    
    # This method runs before all other methods(get, post ,...) and if the user had
    # logged in we will not let him to access the reister page via direct link.
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, "you registered successfully", "success")
            return redirect("home:home")
        # if the data of the form would be invalid(like empty...) form gets
        # new data with messages. we can use that data and render a new page
        # for showing them to user.
        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"
    
    # This method runs before all other methods(get, post ,...) and if the user had
    # logged in we will not let him to access the reister page via direct link.
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})
            
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')