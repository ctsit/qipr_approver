"""
This file is for use when running migrations. for some reason they fail
when the app urls are commented in
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    # url(r'^', include('approver.urls', namespace='approver')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
