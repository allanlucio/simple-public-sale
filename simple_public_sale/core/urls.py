"""simple_public_sale URL Configuration

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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from core.views import *

urlpatterns = [

    path('send-message/', send_message),
    path('list/events', list_all_events),
    re_path('watch/event/(?P<group_id>.+)', watch_event, name='watch-event'),
    re_path('manage/event/(?P<evento_id>.+)', manage_event, name='manage-event'),

]