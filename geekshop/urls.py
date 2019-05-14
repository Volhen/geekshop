from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^', include('mainapp.urls', namespace='main')),
    re_path(r'^auth/', include('authapp.urls', namespace='auth')),
    re_path(r'^basket/', include('basketapp.urls', namespace='basket')),
    re_path(r'^myadmin/', include('adminapp.urls', namespace='myadmin')),
    re_path(r'^order/', include('ordersapp.urls', namespace='order')),

    re_path(r'^auth/verify/vk/oauth2/', include("social_django.urls", namespace="social")),
    
    # path('', include('social_django.urls', namespace='social')),


    # path('admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]