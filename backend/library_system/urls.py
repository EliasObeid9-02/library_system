from django.urls import path, include

from rest_framework.routers import DefaultRouter

from library_system import views, apps

app_name = apps.app_name
