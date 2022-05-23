from django.db import models
from django.conf import settings


class TitleDescriptionMixin(models.Model):
    title = models.CharField(
        'Название',
        help_text='Максимум 150 символов',
        max_length=150,
        unique=True
    )
    
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(
        'URL',
        max_length=50,
        unique=True
    )
    
    class Meta:
        abstract = True
    

class IsActiveMixin(models.Model):
    is_active = models.BooleanField(
        'Активно',
        default=False
    )
    
    class Meta:
        abstract = True
    

class UserRoleMixin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
