from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('manager/', include('manager.urls', namespace='manager')),
    path('', include('homepage.urls', namespace='homepage'))
]

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')), )
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
