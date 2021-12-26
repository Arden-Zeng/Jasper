"""Jasper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from pages.views import home_page
from pages.views import register_page
from pages.views import login_page
from pages.views import logout_page
from pages.views import profile_page
from pages.views import save_post
from pages.views import search_page
from pages.views import modify_interest

from reddit.models import Post

urlpatterns = [
    path(
    "favicon.ico",
    RedirectView.as_view(url=staticfiles_storage.url("jasper-logo.png")),
    ),
    path('', home_page, name = 'home_page'),
    path('register/', register_page, name = 'register_page'),
    path('login/', login_page, name = 'login_page'),
    path('logout/', logout_page, name = 'logout_page'),
    path('profile/', profile_page, name = 'profile_page'),
    path('modifyinterest/', modify_interest, name = 'modify_interest'),
    path('savepost/', save_post, name = 'save_post'),
    path('search/', home_page),
    path('search/<str:searchTerm>', search_page, name = 'search_page'),
    path('admin/', admin.site.urls),
]
