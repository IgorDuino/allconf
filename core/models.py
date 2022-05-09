from django.db import models


class TitleDescriptionMixin(models.Model):
    title = models.CharField('Название', help_text='Макс 150 символов', max_length=150)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        abstract = True
