# Django Imports
from django.urls import re_path
# Wagtail Imports
from wagtailcache.cache import cache_page
# Django COS Imports
from django_cos.views import search

urlpatterns = [
    re_path(r'', cache_page(search), name='django_cos_search'),
]
