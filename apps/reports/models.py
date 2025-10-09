from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
from datetime import datetime
import random, string

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

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
    
    tracking_id = models.CharField(max_length=20, null=True, unique=True, editable=False, db_index=True)
    
    victim_name = models.CharField(max_length=200, blank=True, null=True)    
    is_anonymous = models.BooleanField(default=True)

    assaulter_name = models.CharField(max_length=255, blank=True, null=True)
    assaulter_description = models.TextField(blank=True, null=True,)
    location = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='reports')
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')    
    incident_date = models.DateTimeField()
    description = models.TextField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')


    def generate_tracking_id(self):
        year = datetime.now().year

        count = Report.objects.filter(
            created_at__year=year
        ).count() + 1
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


        return f"SR-{year}-{count:06d}-{random_part}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()
        
        if self.victim_name and not self.is_anonymous:
            if not self.victim_name.startswith('gAAAAA'):
                self.victim_name = self.encrypt_field(self.victim_name)
        
        if self.description and not self.description.startswith('gAAAAA'):
            self.description = self.encrypt_field(self.description)

        if self.assaulter_name and not self.assaulter_name.startswith('gAAAAA'):
            self.assaulter_name = self.encrypt_field(self.assaulter_name)
        super().save(*args, **kwargs)
    
    def get_decrypted_description(self):
        try:
            return self.decrypt_field(self.description)
        except Exception:
            return "[Unable to decrypt]"
        
    def get_decryped_name(self):
        if self.victim_name and not self.is_anonymous:
            try:
                return self.decrypt_field(self.victim_name)
            except:
                return "Error decrypting"
        return "Anonymous"
    
    def get_decrypted_assaulter_name(self):
        if self.assaulter_name:
            try:
                return self.decrypt_field(self.assaulter_name)
            except:
                return "Error decrypting"
        return "Not provided"
    
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
    
    def __str__(self):
        return f"Report {self.tracking_id} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_view_reports", "Can view confidential reports"),
        ]




