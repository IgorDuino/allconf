from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from manager.models import Conference, Lecture
from django.forms.widgets import TextInput, DateInput, TimeInput


User = get_user_model()


class ConferenceCreateForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата проведения',
        widget=TextInput(attrs={'type': 'date', })
    )

    class Meta:
        model = Conference
        fields = ('title', 'description', 'slug', 'category', 'date', 'upload')


class ConferenceChangeForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('description', 'category', 'date', 'upload')


class LectureCreateForm(forms.ModelForm):
    desired_time = forms.TimeField(
        label='Желаемое время',
        required=False,
        input_formats=settings.TIME_INPUT_FORMATS,
        widget=TextInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Lecture
        fields = ('title', 'description', 'slug', 'conference',
                  'category', 'desired_time', 'file')
