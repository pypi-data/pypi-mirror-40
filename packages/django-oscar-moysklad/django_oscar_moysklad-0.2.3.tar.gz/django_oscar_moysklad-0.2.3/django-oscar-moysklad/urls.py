from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # url(r'^products$', views.ProductList.as_view(), name='product.py-list'),
    url(r'^productfolder', views.SyncProductFolder.as_view(), name='product_folder'),
 ]

urlpatterns = format_suffix_patterns(urlpatterns)