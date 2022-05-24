from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from manager.models import Conference, Lecture


User = get_user_model()


class ConferenceCreateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(format=settings.DATE_INPUT_FORMATS))
    
    class Meta:
        model = Conference
        fields = ('title', 'description', 'slug', 'category', 'date', 'upload')


class LectureCreateForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title', 'description', 'slug', 'conference', 'category', 'desired_time', 'file')
    