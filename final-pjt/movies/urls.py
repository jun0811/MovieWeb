from django.urls import path
from . import views

urlpatterns = [
    path('tmdbdata/', views.tmdbdata),
]