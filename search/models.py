from django.db import models
from django.conf import settings
from services.models import Service

# Create your models here.
class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="search_history")
    query = models.CharField(max_length=255)   
    lat = models.FloatField()
    lng = models.FloatField()
    radius_km = models.FloatField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} searched '{self.query}'"


class SearchResult(models.Model):
    search = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name="results")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="search_results")
    distance_km = models.FloatField()   # distance from search location

    def __str__(self):
        return f"Result: {self.service.name} ({self.distance_km:.2f} km)"
