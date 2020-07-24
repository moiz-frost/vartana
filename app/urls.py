from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app import views

# router = DefaultRouter()
router = routers.SimpleRouter()
router.register(r'^form/(?P<form_type>[-\w]+)', views.FormViewSet, basename='form')

# router.register('forms', views.FormViewSet)

urlpatterns = [
    path('', include(router.urls))
]
