from django.urls import path
from manager.views import ConfView, LectureView, CreateConferenceView, CreateLectureView, ConfAdminView

app_name = 'manager'
urlpatterns = [
    path(
        'create/conf/',
        CreateConferenceView.as_view(),
        name='conf-create'),
    path(
        'create/lecture/',
        CreateLectureView.as_view(),
        name='lecture-create'),
    path(
        '<slug:conf_slug>/admin/',
        ConfAdminView.as_view(),
        name='conf-admin'),
    path(
        '<slug:conf_slug>/<slug:lecture_slug>/',
        LectureView.as_view(),
        name='lecture-detail'),
    path(
        '<slug:conf_slug>/',
        ConfView.as_view(),
        name='conf-detail')]
