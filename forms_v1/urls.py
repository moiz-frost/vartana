from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from forms_v1 import views

# router = DefaultRouter()
router = routers.SimpleRouter()
router.register(r'^form/(?P<form_type>[-\w]+)', views.FormViewSet, basename='form')
router.register(r'^form_1040', views.TaxForm1040ViewSet)

urlpatterns = [
    path('', include(router.urls))
]
