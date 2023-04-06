"""unload_sort URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from main.views import main, sort_unload_views, add_xml_view
from download_file.views import save_domain, uoload_file_view
from auth.views import register_view, success_register, login_view, success_login, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/', main, name='main'),
    path('add-domain/', save_domain),
    path('registration/', register_view, name='register'),
    path('success-registartion/', success_register),
    path('login/', login_view, name='login'),
    path('success-login/', success_login),
    path('logout/', logout_view, name='logout'),
    path('upload-data/', uoload_file_view),
    path('sort-unload/', sort_unload_views),
    path('add-xml-proxy/', add_xml_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)