# Django Imports
from django.urls import include, path, re_path
# Wagtail Imports
from wagtail.admin import urls as wagtailadmin_urls
from wagtailimportexport import urls as wagtailimportexport_urls
# Django COS Imports
from django_cos.views import import_pages_from_csv_file


urlpatterns = [
    path('django-cos/import-export/import_from_csv/', import_pages_from_csv_file, name="import_from_csv"),
    re_path(r'', include(wagtailadmin_urls)),
    re_path(r'', include(wagtailimportexport_urls)),
]
