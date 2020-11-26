from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    # profile이 update보다 아래에 있어야 문제가 없음 .... 
    path('password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),
    path('<username>/', views.profile, name='profile'),
]
