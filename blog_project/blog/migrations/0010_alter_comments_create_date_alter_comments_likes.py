# Generated by Django 4.2.5 on 2023-10-02 20:04

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_alter_comments_create_date_remove_comments_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 2, 20, 4, 6, 281800, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
