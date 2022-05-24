from django.db import models


class TitleDescriptionMixin(models.Model):
    title = models.CharField(
        'Название',
        help_text='Максимум 150 символов',
        max_length=150,
        unique=True
    )
    
    description = models.TextField(
        'Описание'
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
