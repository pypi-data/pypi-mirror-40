# Django Imports
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
# Wagtail Imports
from wagtail.documents import urls as wagtaildocs_urls
# Django COS Imports
from django_cos import urls as django_cos_urls
from django_cos import admin_urls as django_cos_admin_urls
from django_cos import search_urls as django_cos_search_urls

urlpatterns = [
    # Admin
    path('django-admin/', admin.site.urls),
    path('admin/', include(django_cos_admin_urls)),

    # Documents
    path('docs/', include(wagtaildocs_urls)),

    # Search
    path('search/', include(django_cos_search_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(django_cos_urls)),

    # Alternatively, if you want CMS pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(django_cos_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
