from django.urls import path
from .views import SupportContactListAPIView

urlpatterns = [
    path('', SupportContactListAPIView.as_view(), name='support'),
]
