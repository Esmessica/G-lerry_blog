from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comments
from blog.forms import PostForm, CommentsForm, RegisterForm
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
# v for like functionality
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Add any additional logic you want here
        return response

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

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


class DraftListView(LoginRequiredMixin, ListView):

    login_url = 'login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')
    """
    Creates query to make sure those posts does not have any published date
    """

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("Queryset count:", queryset.count())  # Print the count of the queryset
        return super().get(request, *args, **kwargs)

    """
    If we wanted to fetch data not using default value object_list,
    we can use code below to change that hwo we like
    """
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts'] = context['object_list']
    #     return context


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'registration/register.html', {'form': form})


"""
Comments views here
"""


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)

    # Check if the user has already liked the comment
    if comment.likes.filter(id=request.user.id).exists():
        # User already liked the comment, so unlike it
        comment.likes.remove(request.user)
        liked = False
    else:
        # User hasn't liked the comment, so like it
        comment.likes.add(request.user)
        liked = True

    likes_count = comment.likes.count()
    comment.save()

    return JsonResponse({'likes': likes_count, 'liked': liked})

# @csrf_exempt
# @require_POST
# def like_comment(request, pk):
#     comment = get_object_or_404(Comments, pk=pk)
#     comment.increment_likes()
#     likes_count = comment.likes
#     return JsonResponse({'likes': likes_count})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentsForm()
    return render(request, 'blog/comments_form.html', {'form':form})

"""
Request and pk links comment to post, get post object or 404 page, pass in post model
If someone  submited the form, form is equal to CommentsForm.
If form is valid, save,comment.post make it equal to t he post field
else just return comment html
"""


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()       # function from models.py
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

