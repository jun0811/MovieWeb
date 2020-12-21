from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('tmdbdata/', views.tmdbdata),
    path('', views.index, name='index'),
    path('<int:pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<genre>/search/', views.search_genre, name= 'search_genre'),
    path('topratedlist/<int:page>', views.top_ratedlist, name='top_ratedlist'),
    path('search/<input>/', views.search, name='search'),
    
]