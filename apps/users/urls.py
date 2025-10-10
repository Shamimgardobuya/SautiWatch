from django.urls import path
from .views import  RegisterView, LoginView, LogoutView, CurrentUserView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('list/', UserListView.as_view(), name='user-list'),


]
