from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from forms_v2 import views

# router = DefaultRouter()
router = routers.SimpleRouter()
router.register(r'^form_definition', views.FormDefinitionViewSet, basename='form_definition')
router.register(r'^form_instance', views.FormInstanceViewSet, basename='form_instance')

urlpatterns = [
    path('', include(router.urls))
]
