from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserRegisterView(View):
    # Class variables for clean code purpose.
    form_class = UserRegistrationForm
    template_name = "account/register.html"

    # This method runs before all other methods(get, post ,...) and if the user had
    # logged in we will not let him to access the reister page via direct link.
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home:home")
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
    # logged in we will not let him to access the login page via direct link.
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully", "success")
                return redirect("home:home")
            messages.error(request, "username or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    # For abstaning/avoiding the user from accessing logout address we have to use
    # LoginRequiredMixin and below variable or LOGIN_URL in settings.py for redirecting
    # the user to login.html page.

    # login_url = "/account/login/"
    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", "success")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        # get() will return only one record and if there are more records it will raise
        # an error.
        user = get_object_or_404(User, id=user_id)
        # filter() will return 0 or more records in a query-set/list.
        posts = Post.objects.filter(user=user)
        return render(request, "account/profile.html", {"user": user, "posts": posts})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    # The data that will be send to the user.
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    # After sending an email for user we'll show this html page to user.
    template_name = "account/password_reset_done.html"
    
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
