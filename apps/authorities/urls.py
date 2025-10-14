from django.urls import path
from .views import AuthorityListCreateView, AuthorityDetailView

urlpatterns = [
    path('', AuthorityListCreateView.as_view(), name='authority-list'),
    path('<int:pk>/', AuthorityDetailView.as_view(), name='authority-detail'),
]
