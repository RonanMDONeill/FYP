"""PaperMill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path, re_path

from pages.views import register_view, login_view, home_view, main_view
from collection.views import colllist_view, collcreate_view, coll_view

# Define the base URL paths

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_view),
    path('home/', home_view, name='home'),
    path('', main_view, name='main'),
    path('search/', include('search.urls')),
    path('vis/', include('vis.urls')),
    path('collection/', include('collection.urls')),
    path('rec/', include('recommendation.urls')),
    path('external/', include('external.urls')),
]
