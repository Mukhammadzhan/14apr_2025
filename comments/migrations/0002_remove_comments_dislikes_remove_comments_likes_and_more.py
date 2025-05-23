# Generated by Django 5.1.7 on 2025-05-17 05:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='likes',
        ),
        migrations.AddField(
            model_name='comments',
            name='users_disliked',
            field=models.ManyToManyField(blank=True, related_name='comments_disliked', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи, поставившие дизлайк'),
        ),
        migrations.AddField(
            model_name='comments',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='comments_liked', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи, поставившие лайк'),
        ),
    ]
