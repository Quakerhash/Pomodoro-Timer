"""
URL configuration for temp project.

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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from . import views
from django.shortcuts import redirect
urlpatterns = [
    path('',include('login.urls')),
    path('admin/', admin.site.urls),
    path('Home/',views.HOME,name='home'),
    path('About/',views.ABOUT,name="about"),
    path('', lambda request: redirect('register/')),
    path('Learn/',include('Learn.urls')),
    path('StudyStratergies/',views.ss,name="ss"),
    path('Timer/',views.Timer,name="Timer"),
    path('Progess/',views.Progress,name="Progress"),

]
