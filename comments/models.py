from django.db import models
from django.utils import timezone

from clients.models import Client
from posts.models import Posts


class Comments(models.Model):
    post = models.ForeignKey(
        to=Posts,
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name="статья",
    )
    user = models.ForeignKey(
        to=Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_comments",
        verbose_name="автор комментария",
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_comments",
        verbose_name="родительский комментарий",
    )
    text = models.TextField(
        verbose_name="текст комментария",
        max_length=2000,
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    users_liked = models.ManyToManyField(
        to=Client,
        related_name="comments_liked",
        verbose_name="Пользователи, поставившие лайк",
        blank=True,
    )
    users_disliked = models.ManyToManyField(
        to=Client,
        related_name="comments_disliked",
        verbose_name="Пользователи, поставившие дизлайк",
        blank=True,
    )
    

    def total_likes(self):
        return self.users_liked.count()

    def total_dislikes(self):
        return self.users_disliked.count()

    class Meta:
        ordering = ("id",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"{self.user} | {self.text[:20]}..."