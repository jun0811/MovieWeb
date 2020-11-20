from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path('',views.index, name="index"),
    path('create/',views.create, name="create"),
    path('<int:pk>/',views.detail, name="detail"),
    path('<int:pk>/update',views.detail, name="update"),
    path('<int:pk>/delete',views.detail, name="delete"),
]
