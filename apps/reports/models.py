from django.db import models
from apps.authorities.models import Authority
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.contrib.auth import get_user_model

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Report(models.Model):
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
    ]
    
    victim_name = models.CharField(max_length=200, blank=True, null=True)    
    location = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='reports')
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')    
    incident_date = models.DateTimeField()
    description = models.TextField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    assigned_to = models.ForeignKey(Authority, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')
    

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_view_reports", "Can view confidential reports"),
            ("can_manage_reports", "Can manage and update reports"),
        ]
    
    def __str__(self):
        return f"Report #{self.id} - {self.get_urgency_level_display()} - {self.created_at.strftime('%Y-%m-%d')}. Case of {self.description}"
    
    def save(self, *args, **kwargs):
        if self.description and not self.description.startswith('gAAAAA'):
            self.description = self.encrypt_field(self.description)
        super().save(*args, **kwargs)
    
    def get_decrypted_description(self):
        try:
            return self.decrypt_field(self.description)
        except Exception:
            return "[Unable to decrypt]"
    
    @staticmethod
    def encrypt_field(value):
        key = settings.ENCRYPTION_KEY
        f = Fernet(key)
        return f.encrypt(value.encode()).decode()
    
    @staticmethod
    def decrypt_field(value):
        key = settings.ENCRYPTION_KEY
        f = Fernet(key)
        return f.decrypt(value.encode()).decode()



class AuditLog(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
    

