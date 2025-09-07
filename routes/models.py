from django.db import models
from django.conf import settings
from services.models import Service

class Route(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="routes")
    origin_lat = models.FloatField()
    origin_lng = models.FloatField()
    dest_lat = models.FloatField()
    dest_lng = models.FloatField()
    distance_km = models.FloatField()
    duration_min = models.FloatField()
    geometry = models.JSONField()
    steps = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route by {self.user.email} ({self.origin_lat},{self.origin_lng} -> {self.dest_lat},{self.dest_lng})"


class RouteService(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    distance_km = models.FloatField()

    def __str__(self):
        return f"{self.service.name} on route {self.route.id} ({self.distance_km:.2f} km)"
