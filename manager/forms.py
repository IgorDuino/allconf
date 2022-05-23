from django import forms
from django.contrib.auth import get_user_model
from manager.models import Conference, Lecture


User = get_user_model()


class ConferenceCreateForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('title', 'description', 'slug', 'category', 'date')


class LectureCreateForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title', 'description', 'slug', 'conference', 'category', 'file')
