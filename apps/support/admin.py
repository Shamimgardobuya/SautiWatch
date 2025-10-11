from django.contrib import admin
from .models import SupportContact

# Register your models here.
@admin.register(SupportContact)
class SupportContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region', 'is_verified')