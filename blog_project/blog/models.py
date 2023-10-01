from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.


class Post(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # author is linked to authorized user = someone who can create new post
    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, null=True)
    # text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    # By default, it takes timezone from settings.py
    published_date = models.DateTimeField(blank=True, null=True)
    # Blank becouse you don't have to oublish it rightaway, null-can never be published

    def publish(self):  # function to publish Post
        self.published_date = timezone.now()
        self.save()
        # published date is now

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        # filter comments to be approved then show them

    def get_absolute_url(self):
        # has to have the get_Absolute_url name
        return reverse('post_detail', kwargs={'pk': self.pk})

    """ 
        The primary key patches to self.pk, after i create post, and i hit publication, 
        go to post detail of the primary key of post i just created
        
    """

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    # Connected to blog Post key, name is set up to comments, connect each comment to actual post in future
    author = models.CharField(max_length=100)
    # not the same author as in Post class
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    # Automatically set date for today, now
    approved_comment = models.BooleanField(default=False)
    # By default, says approved comment is not approved,
    # it should be the same name as in approve_comments functions return
    likes = models.PositiveIntegerField(default=0)

    def increment_likes(self):
        self.likes += 1
        self.save()

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    """
        After post comment, go back to list of all posts,
        comment has to be approved before being there
    """

    def __str__(self):
        return self.text
