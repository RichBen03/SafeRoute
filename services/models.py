from django.db import models

# Create your models here.
class Service(models.Model):
    SERVICE_TYPES = [
        ("hospital", "Hospital"),
        ("police", "Police Station"),
        ("fire", "Fire Station"),
        ("pharmacy", "Pharmacy"),
        ("school", "School"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
