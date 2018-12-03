from django.conf import settings
from django.contrib import admin
from django.urls import include, path


# TODO: the path of applications that are not indclude in INSTALL_APPS
# must be removed before migrate in production!
urlpatterns = [
    path('', include('website.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('cosinesimulation/', include('cosinesimulation.urls')),
    path('scorebasedrecommend/', include('scorebasedrecommend.urls')),
    path('collaborative/', include('collaborative.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
