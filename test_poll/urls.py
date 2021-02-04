from django.contrib import admin
from django.urls import path, include

from test_poll import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('poll.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
