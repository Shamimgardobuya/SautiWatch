from django.contrib import admin
from .models import Report, Region

# Register your models here.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'location', 'region', 'urgency_level', 'status', 'created_at', 'is_anonymous']
    list_filter = ['status', 'urgency_level', 'region', 'created_at', 'is_anonymous']
    search_fields = ['tracking_id', 'location', 'description']
    readonly_fields = ['tracking_id', 'created_at', 'updated_at',]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Identification', {
            'fields': ('tracking_id', 'is_anonymous', 'victim_name')
        }),
        ('Assaulter Information', {
            'fields': ('assaulter_name', 'assaulter_description')
        }),
        ('Incident Details', {
            'fields': ('location', 'region', 'incident_date', 'description', 'urgency_level')
        }),
        ('Case Management', {
            'fields': ('status', 'encrypted_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('region')