# Generated by Django 4.2.5 on 2023-09-25 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 25, 20, 5, 23, 468594, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 25, 20, 5, 23, 417645, tzinfo=datetime.timezone.utc)),
        ),
    ]
