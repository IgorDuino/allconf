from django.db import models
from core.models import TitleDescriptionMixin
from django.core.files.storage import FileSystemStorage


storage = FileSystemStorage(location='/media/file')


class Category(TitleDescriptionMixin):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Conference(TitleDescriptionMixin):
    date = models.DateField('Дата проведения')
    category = models.ForeignKey(Category, verbose_name='Категории', on_delete=models.SET_NULL,
                                 related_name='conferences', null=True)

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'


class Lecture(TitleDescriptionMixin):
    desired_time = models.DateTimeField('Желаемое время', null=True, blank=True)
    file = models.FileField('Презентация', storage=storage)
    conference = models.ForeignKey(Conference, verbose_name='Лекции', on_delete=models.CASCADE, related_name='lectures')
    category = models.ForeignKey(Category, verbose_name='Категории', on_delete=models.SET_NULL,
                                 related_name='lectures', null=True)

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'
