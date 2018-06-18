"""SleepProj URL Configuration"""

from django.contrib import admin
from django.urls import path, re_path

import app
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', app.views.dataSleep),
]
