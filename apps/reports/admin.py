from django.contrib import admin
from .models import Report, Region, AuditLog

# Register your models here.
admin.site.register(AuditLog)
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact_email', 'contact_phone']
    search_fields = ['name', 'code']




@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'urgency_level', 'status', 'region', 'created_at', 'assigned_to']
    list_filter = ['status', 'urgency_level', 'region', 'created_at']
    search_fields = ['location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('victim_name', 'location', 'region', 'urgency_level')
        }),
        ('Incident Details', {
            'fields': ('incident_date', 'description')
        }),
        ('Status', {
            'fields': ('status', 'assigned_to')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser