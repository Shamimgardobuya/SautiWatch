from django.db import models

# Create your models here.

class Authority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=70, null=True)
    email = models.EmailField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    state_phone_number = models.CharField(max_length=50, blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = "Authorities"