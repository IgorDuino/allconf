from django.db import models
from django.db.models import Prefetch
from core.models import TitleDescriptionMixin, SlugMixin, IsActiveMixin
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import get_thumbnail
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator


class Category(MPTTModel, TitleDescriptionMixin, SlugMixin, IsActiveMixin):
    title = models.CharField(
        'Название',
        help_text='Макс 70 символов',
        max_length=70,
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительская категория',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subcategories'
    )

    def __str__(self):
        return self.title[:20]

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class ConferenceManager(models.Manager):
    def get_active(self):
        queryset = self.get_queryset().filter(is_active=True)
        
        return queryset
    
    def get_conference_with_lectures(self):
        queryset = self.get_active().prefetch_related(
            Prefetch('lectures', queryset=Lecture.objects.filter(is_active=True))
        )
        
        return queryset
            
    def get_conference_with_lectures_and_category(self):
        queryset = self.get_active().prefetch_related(
            Prefetch('lectures', queryset=Lecture.objects.filter(is_active=True))
        ).select_related('category')
        
        return queryset



class Conference(TitleDescriptionMixin, SlugMixin, IsActiveMixin):
    date = models.DateField('Дата проведения')
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.SET_NULL,
        related_name='conferences',
        null=True
    )
    upload = models.ImageField(
        'Главное изображение',
        upload_to='uploads/',
        null=True
    )
    
    def get_image_x1280(self):
        return get_thumbnail(self.upload, '1280', quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.upload, '400x300', crop='center', quality=51)

    def image_tmb(self):
        if self.upload:
            return mark_safe(
                f'<img src="{self.upload.url}", width="50">'
            )
        return 'Нет изображения'
    
    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'

    objects = ConferenceManager()


class Lecture(TitleDescriptionMixin, SlugMixin, IsActiveMixin):
    desired_time = models.TimeField(
        'Желаемое время',
        null=True,
        blank=True
    )
    file = models.FileField(
        'Презентация',
        upload_to='files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    conference = models.ForeignKey(
        Conference,
        verbose_name='Конференция',
        on_delete=models.CASCADE,
        related_name='lectures'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.SET_NULL,
        related_name='lectures',
        null=True
    )
    confirmed = models.BooleanField(
        'Утверждена',
        default=False
    )

    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'