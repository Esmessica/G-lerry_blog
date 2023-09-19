from django.shortcuts import render
from blog.models import Post, Comments
from django.views.generic import (TemplateView, ListView)

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