from django.contrib import admin
from django.urls import path, include

from test_poll import settings
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('poll.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
