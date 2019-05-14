from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),
    # re_path(r'^catalog/$', mainapp.catalog, name='catalog'),
    re_path(r'^category/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.category, name='category'),
    re_path(r'^card/(?P<pk>\d+)/$', mainapp.card, name='card'),
    re_path(r'^contacts/$', mainapp.contacts, name='contacts'),
]

