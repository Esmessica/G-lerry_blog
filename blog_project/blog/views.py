from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comments
from blog.forms import PostForm, CommentsForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


# Create your views here.

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


"""
Comments views here
"""

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

