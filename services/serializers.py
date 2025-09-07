from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


#serializer for geocoding
class GeocodeSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)
