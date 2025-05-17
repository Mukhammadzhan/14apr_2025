from clients.validators import (
    validate_email_domain,
    validate_username,
    validate_password
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission,
)

class ClientManager(BaseUserManager):
    def create_superuser(
            self,
            username:str,
            email:str,
            password:str,
    ) -> "Client":
        """Create super user."""
        
        validate_username(username)
        validate_email_domain(email)
        validate_password(password)
        
        client = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        client.set_password(raw_password=password)
        client.save(using=self._db)
        return client


class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="никнейм",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="эл. почта",
        max_length=100,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name="активный",
        default=False,
    )
    activation_code = models.CharField(
        verbose_name="код активации",
        max_length=100,
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(
        verbose_name="сотрудник",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="администратор",
        default=False,
    )
    gender = models.CharField(
        verbose_name="пол",
        max_length=10,
        blank=True,
        null=True,
        choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Другой')],
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    groups = models.ManyToManyField(
        Group,
        related_name="client_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="client_permissions",
        blank=True
    )
    avatar = models.ImageField(
        verbose_name="аватар",
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = ClientManager()
    def get_full_name(self) -> str:
        """Return full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        """Return short name."""
        return self.first_name or self.username

    def delete_account(self):
        """Soft delete account."""
        self.is_active = False
        self.save()
    
    class Meta:
        ordering = ("id",)
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.username}  | {self.email} | {self.date_created}"
