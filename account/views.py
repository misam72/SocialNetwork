from typing import Any
from django import http
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
from .models import Relation


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

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # with next value that is in url we can redirect the user to last page that he has seen
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
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
                if self.next:
                    # with using self.next we redirect user to the page that he had been on it befor login.
                    return redirect(self.next)
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
        is_following = False
        # get() will return only one record and if there are more records it will raise
        # an error.
        user = get_object_or_404(User, id=user_id)
        # filter() will return 0 or more records in a query-set/list.
        # posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user_id)
        if relation.exists():
            is_following = True
        # using backward relation
        posts = user.posts.all()
        return render(request, "account/profile.html", {"user": user, "posts": posts,
                                                        "is_following": is_following})


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



class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'you followed this user', 'success')
        return redirect('account:user_profile', user_id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you did not follow this user', 'danger')
        return redirect('account:user_profile', user_id)
