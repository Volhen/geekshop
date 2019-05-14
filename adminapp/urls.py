from django.urls import path, re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # re_path(r'^$', adminapp.index, name='index'),
     re_path(r'^$', adminapp.UsersListView.as_view(), name='index'),

    re_path(r'^shopuser/create/$', adminapp.shopuser_create, name='shopuser_create'),
    re_path(r'^shopuser/update/(?P<pk>\d+)/$', adminapp.shopuser_update, name='shopuser_update'),
    re_path(r'^shopuser/delete/(?P<pk>\d+)/$', adminapp.shopuser_delete, name='shopuser_delete'),
    re_path(r'^shopuser/recover/(?P<pk>\d+)/$', adminapp.shopuser_recover, name='shopuser_recover'),
    
    re_path(r'^categories/$', adminapp.categories, name='categories'),
    # re_path(r'^productcategory/create/$', adminapp.productcategory_create, name='productcategory_create'),
    re_path(r'^productcategory/create/$', adminapp.ProductCategoryCreateView.as_view(), name='productcategory_create'),
    # re_path(r'^productcategory/update/(?P<pk>\d+)/$', adminapp.productcategory_update, name='productcategory_update'),
    re_path(r'^productcategory/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='productcategory_update'),
    # re_path(r'^productcategory/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='productcategory_delete'),
    re_path(r'^productcategory/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='productcategory_delete'),

    re_path(r'^cards/(?P<pk>\d+)/$', adminapp.cards, name='cards'),
    re_path(r'^card/create/(?P<pk>\d+)/$', adminapp.card_create, name='card_create'),
    # re_path(r'^card/read/(?P<pk>\d+)/$', adminapp.card_read, name='card_read'),
    re_path(r'^card/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='card_read'),
    re_path(r'^card/update/(?P<pk>\d+)/$', adminapp.card_update, name='card_update'),
    re_path(r'^card/delete/(?P<pk>\d+)/$', adminapp.card_delete, name='card_delete'),


]
