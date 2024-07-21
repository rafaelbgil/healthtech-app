from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    #api endpoints
    path('agenda/', views.MedicoAgendaView.as_view()),
    path('agenda/<str:uuid>/', views.MedicoAgendaDetalhesView.as_view()),
]