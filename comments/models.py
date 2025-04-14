from django.db import models
from django.utils import timezone

from clients.models import Client

class Comments(models.Model):
    author = models.CharField(
        verbose_name="ФИО Автора",
        max_length=100,
    )
    text = models.CharField(
        verbose_name="Текст",
        max_length=5000,
    )
    likes = models.PositiveBigIntegerField(
        verbose_name="лайки",
        default=0,
    )
    dislikes = models.PositiveBigIntegerField(
        verbose_name="дизлайки",
        default=0,
    )
    data_coments = models.DateTimeField(
        verbose_name="Дата коментарии",
        default=timezone.now(),
    )
    parent_comment = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='replies',
        verbose_name="Родительский комментарий"
    )

    def __str__(self):
        return f'Комментарий {self.id} от {self.author}'
    


