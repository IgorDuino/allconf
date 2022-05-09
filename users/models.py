from django.db import models
from manager.models import Lecture, Conference
from core.models import UserRoleMixin


class Speaker(UserRoleMixin):
    lecture = models.OneToOneField(Lecture, verbose_name='Лекция', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Докладчик'
        verbose_name_plural = 'Докладчики'


class ConferenceOrganizer(UserRoleMixin):
    conference = models.OneToOneField(Conference, verbose_name='Конференция', on_delete=models.CASCADE)


class ConferenceModerator(UserRoleMixin):
    change_category = models.BooleanField('Возможность изменять категорию конференции', default=False)
    change_identity = models.BooleanField('Возможность изменять айдентику', default=False)
    change_date = models.BooleanField('Возможность изменять дату проведения конференции', default=False)
    manage_speakers = models.BooleanField('Возможность управлять докладчиками', default=False)
    change_landing = models.BooleanField('Возможность изменять лендинг конференции', default=False)
    conference = models.OneToOneField(Conference, verbose_name='Конференция', on_delete=models.CASCADE)


class Listener(UserRoleMixin):
    arrival_time = models.DateTimeField('Время прихода', null=True, blank=True)
    conference = models.OneToOneField(Conference, verbose_name='Конференция', on_delete=models.CASCADE)
