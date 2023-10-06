from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, "home/detail.html", {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "post deleted successfully", "success")
        else:
            messages.error(request, "you can not delete this post", "danger")
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    
    # setup() method will be ruuning before all other methods like dispatch ,...
    # We will defind **post_instance** here for making performance better. Here we 
    # connect to database only one time instead of connecting it in each method.
    def setup(self, request, *args: Any, **kwargs: Any):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    # In this method we will not allowing the users that not owned the posts from 
    # changing them.
    def dispatch(self, request, *args: Any, **kwargs: Any):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, 'you are not allowed to update this post', 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    # **post_id** will be in kwargs. We do not need post_id but we have to get it in 
    # our methods(it comes with calling the url of this api).
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})
    
    # **post_id** will be in kwargs. We do not need post_id but we have to get it in 
    # our methods(it comes with calling the url of this api).
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            # We have to save slug manually, because it will not be generated 
            # automatically.
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'You successfully updated this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you successfully created a post','success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
  