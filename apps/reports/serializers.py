from rest_framework import serializers
from .models import Report, Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'code']

class ReportSerializer(serializers.ModelSerializer):
    victim_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    decrypted_victim_name = serializers.SerializerMethodField(read_only=True)
    decrypted_description = serializers.SerializerMethodField(read_only=True)
    decrypted_assaulter_name = serializers.SerializerMethodField(read_only=True)

    region_name = serializers.CharField(source='region.name', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'tracking_id',
            'victim_name',
            'decrypted_victim_name',
            'is_anonymous',
            'assaulter_name',
            'decrypted_assaulter_name',
            'assaulter_description',
            'location',
            'region',
            'region_name',
            'urgency_level',
            'incident_date',
            'description',
            'decrypted_description',
            'status',
            'created_at',
            'updated_at',
            'assigned_to',
            'assigned_to_username'
        ]
        read_only_fields = ['tracking_id', 'created_at', 'updated_at']

    def get_decrypted_victim_name(self, obj):
        return obj.get_decrypted_victim_name()

    def get_decrypted_description(self, obj):
        return obj.get_decrypted_description()

    def get_decrypted_assaulter_name(self, obj):
        return obj.get_decrypted_assaulter_name()

    def create(self, validated_data):
        return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
