from django.shortcuts import render
from blog.models import Post, Comments
from blog.forms import PostForm, CommentsForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now().order_by('-published_date'))

    """
    
    with get query set - set SQL query in model. 
    Grab post model.all objects and filter them based on condition.
    --lte=less than or equal to current tiem and order them based by curent date (the dash means DESC order
    
    """


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):

    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'           # redirect to detail view
    form_class = PostForm
    # mixin require those above
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):

    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'  # redirect to detail view
    form_class = PostForm
    # mixin require those above
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')