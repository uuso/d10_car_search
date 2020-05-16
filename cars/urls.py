from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace="app")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)), 
    ] + urlpatterns
