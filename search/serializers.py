from rest_framework import serializers
from .models import SearchHistory, SearchResult
from services.serializers import ServiceSerializer


class SearchResultSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = SearchResult
        fields = ["id", "service", "distance_km"]

    def get_distance_km(self, obj):
        return round(obj.distance_km, 2)


class SearchHistorySerializer(serializers.ModelSerializer):
    results = SearchResultSerializer(many=True, read_only=True)

    class Meta:
        model = SearchHistory
        fields = ["id", "query", "lat", "lng", "radius_km", "created_at", "results"]


class GeocodeInputSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)


class GeocodeOutputSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    display_name = serializers.CharField()
