from django.db import models
from django.utils import timezone

from clients.models import Client



class Categories(models.Model):
    title = models.CharField(
        verbose_name="Категория",
        max_length=50,
        unique=True,
    )
    

    class Meta:
        ordering = ("id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.pk}  | {self.title}"


class Posts(models.Model):
    title = models.CharField(
        verbose_name="Названия поста",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описания",
        max_length=5000,
    )
    data_publication = models.DateTimeField(
        verbose_name="Дата публикации",
        default=timezone.now,
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
    categories = models.ManyToManyField(
        to=Categories,
        verbose_name="Категории",
        related_name="post_categories",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Статья"
        verbose_name_plural = "Статии"

    def __str__(self):
        return f"{self.title}  | {self.user} | {self.data_publication}"

class Images(models.Model):
    image = models.ImageField(
        verbose_name="изоброжения",
        upload_to="images/posts/",
    )
    post = models.ForeignKey(
        to=Posts, 
        on_delete=models.CASCADE,
        related_name="post_images",
        verbose_name="статья",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изоброжения"
        verbose_name_plural = "изоброжении"

    def __str__(self):
        return f"{self.pk}  | {self.image}"

