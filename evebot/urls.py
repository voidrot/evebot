"""
URL configuration for evebot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.conf import settings

urlpatterns = [
    # path("sitemap.xml", sitemap, {"sitemaps": sitemap}, name="django.contrib.sitemaps.views.sitemap"),
    path("admin/", admin.site.urls),
    re_path(r"^sso/", include("esi.urls", namespace="esi")),
] + debug_toolbar_urls()
