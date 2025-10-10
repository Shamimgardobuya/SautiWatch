from rest_framework import serializers
from .models import Authority

class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = [
            'id',
            'name',
            'state',
            'email',
            'latitude',
            'longitude',
            'phone_number',
            'state_phone_number',
        ]
