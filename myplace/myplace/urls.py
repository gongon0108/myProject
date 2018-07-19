"""myplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from googlecalendar import views
from django.conf import settings

SOCIAL_AUTH_NAMESPACE = 'social'

LOGIN_REDIRECT_URL = '/'

urlpatterns = [
    path('googlecalendar/', include('googlecalendar.urls')),
    path('accounts/profile/', include('googlecalendar.urls')),
    path('googlecalendar/new/', views.post, name='new_calendar'),
    path('', include('social_django.urls', namespace='social')),
    #path('googlecalendar/social', namespace='social'),
    path('admin/', admin.site.urls),
]
