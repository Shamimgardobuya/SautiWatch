from django.urls import path
from .views import SupportContactListCreateAPIView

urlpatterns = [
    path('', SupportContactListCreateAPIView.as_view(), name='support'),
]