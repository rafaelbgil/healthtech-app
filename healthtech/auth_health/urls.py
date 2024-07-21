from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    #api endpoints
    path('', views.AuthView.as_view(), name="authenticacao"),
]