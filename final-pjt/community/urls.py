from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    # path('',views.index, name="index"),
    path('reviews/',views.reviews, name="reviews"), 
    path('create/<movie_id>/',views.create, name="create"),
    path('<int:pk>/update/',views.update, name="update"),
    path('detail/<int:pk>/<movie_title>/',views.detail, name="detail"),
    path('<int:pk>/delete/',views.delete, name="delete"),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('search_title/<str:title>/', views.search_title, name= "search_title"),
]
