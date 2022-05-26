from django.urls import path, include
from homepage.views import HomeView, SearchView

app_name = 'homepage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
]
