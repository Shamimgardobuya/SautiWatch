from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Authority
from .serializers import AuthoritySerializer
# Create your views here.


class AuthorityListCreateView(generics.ListCreateAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    