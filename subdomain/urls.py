from django.urls import path

from subdomain import views

urlpatterns = [
    path("regname/", views.regname, name="regname"),
    path("check/",   views.check,   name="check"),
]

