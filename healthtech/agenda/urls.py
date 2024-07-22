from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    #api endpoints
    path('find_by_especialidade/<str:especialidade>/', views.AgendaFindByEspecialidadeView.as_view()),
    path('<str:uuid>/reservar/', views.AgendaReservarView.as_view()),
]