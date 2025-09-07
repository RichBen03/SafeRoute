from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeocodeSerializer
import requests

class GeocodeView(APIView):
    def post(self, request):
        serializer = GeocodeSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data['address']
            # Example: call OpenStreetMap Nominatim API
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": address, "format": "json", "limit": 1}
            response = requests.get(url, params=params).json()
            if response:
                result = {
                    "address": address,
                    "latitude": response[0]["lat"],
                    "longitude": response[0]["lon"]
                }
                return Response(result, status=status.HTTP_200_OK)
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Custom permission: only staff/admins can write, others read-only
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS → allow anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Non-safe methods → require staff/admin
        return request.user and request.user.is_staff


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing emergency services.
    - Anyone can view (GET, list, retrieve).
    - Only staff/admins can add, update, or delete.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
