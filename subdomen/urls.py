from django.urls import path

from subdomen import views

urlpatterns = [
    path("", views.regname)
]

