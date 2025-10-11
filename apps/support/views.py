from rest_framework import generics
from .models import SupportContact
from .serializers import SupportContactSerializer

class SupportContactListAPIView(generics.ListAPIView):
    serializer_class = SupportContactSerializer

    def get_queryset(self):
        queryset = SupportContact.objects.filter(is_verified=True)
        region = self.request.query_params.get('region', '')
        category = self.request.query_params.get('category', '')

        if region:
            queryset = queryset.filter(region__icontains=region)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
