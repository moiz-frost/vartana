from django.contrib import admin
from django.urls import path

from taxes import views

urlpatterns = [
    path('', views.some_view)
]
