from django.db import models

# Create your models here.
class SupportContact(models.Model):
    CATEGORY_CHOICES = (
    ("Therapist", "Therapist"),
    ("Counsellor", "Counsellor"),
    ("Health", "Health"),
    )

    name = models.CharField(max_length=50)
    organization = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    region = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name