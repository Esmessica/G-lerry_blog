from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # author is linked to authorized user = someone who can create new post
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    # By default, it takes timezone from settings.py
    published_date = models.DateTimeField(blank=True, null=True)
    # Blank becouse you don't have to oublish it rightaway, null-can never be published

    def publish(self):
        # function to publish Post
        self.published_date = timezone.now()
        self.save()
        # published date is now

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)
        # filter comments to be approved then show them

    def __str__(self):
        return self.title