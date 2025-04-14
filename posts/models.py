from django.db import models
from django.utils import timezone

from clients.models import Client




class Posts(models.Model):
    title = models.CharField(
        verbose_name="Названия поста",
        max_length=200,
    )
    description = models.CharField(
        verbose_name="Описания",
        max_length=5000,
    )
    data_publication = models.DateTimeField(
        verbose_name="Дата публикации",
        default=timezone.now(),
    )
    user = models.ForeignKey(
        to=Client,
        verbose_name="Автор",
        on_delete=models.SET_DEFAULT,
        default="Unknown author",
        related_name="client_posts",
    )
    likes = models.PositiveBigIntegerField(
        verbose_name="лайки",
        default=0,
    )
    dislikes = models.PositiveBigIntegerField(
        verbose_name="дизлайки",
        default=0,
    )

class Images(models.Model):
    imaage = models.ImageField(
        verbose_name="изоброжения",
        upload_to="images/posts/",
    )
    post = models.ForeignKey(
        to=Posts, 
        on_delete=models.CASCADE,
        related_name="post_images",
        verbose_name="статья"
    )
