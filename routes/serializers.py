from rest_framework import serializers
from .models import Route, RouteService
from services.serializers import ServiceSerializer

class RouteServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = RouteService
        fields = ["id", "service", "distance_km"]


class RouteSerializer(serializers.ModelSerializer):
    services = RouteServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "origin_lat",
            "origin_lng",
            "dest_lat",
            "dest_lng",
            "distance_km",
            "duration_min",
            "geometry",
            "steps",
            "created_at",
            "services",
        ]
