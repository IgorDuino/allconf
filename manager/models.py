from django.db import models
from django.db.models import Q
from core.models import TitleDescriptionMixin
from django.core.files.storage import FileSystemStorage
from mptt.models import MPTTModel, TreeForeignKey


storage = FileSystemStorage(location='/media/file')


class Category(MPTTModel, TitleDescriptionMixin):
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


class Conference(TitleDescriptionMixin):
    date = models.DateField('Дата проведения')
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.SET_NULL,
        related_name='conferences',
        null=True
    )

    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'


class Lecture(TitleDescriptionMixin):
    desired_time = models.DateTimeField(
        'Желаемое время',
        null=True,
        blank=True
    )
    file = models.FileField(
        'Презентация',
        storage=storage
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

    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name = 'Доклад'
        # verbose_name_plural = 'Доклады'
        # constraints = [
        #     models.CheckConstraint(check=Q(category__parent=Conference.category), name='age_gte_18')
        # ]
