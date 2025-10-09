from django.urls import path
from .views import create_user, login_user, logout_user

urlpatterns = [
    path('register/', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout'),


]
