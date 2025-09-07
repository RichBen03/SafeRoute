from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    GeocodeInputSerializer,
    GeocodeOutputSerializer,
    SearchHistorySerializer,
)
from .models import SearchHistory, SearchResult
from .utilis import normalize_address, geocode_nominatim
from services.models import Service


class GeocodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = GeocodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data["address"]

        # Check cache
        cache_key = f"geocode:{normalize_address(address)}"
        cached = cache.get(cache_key)
        if cached:
            return Response(GeocodeOutputSerializer(cached).data, status=status.HTTP_200_OK)

        # Call Nominatim
        try:
            result = geocode_nominatim(address)
        except Exception as e:
            return Response(
                {"detail": f"Geocoding failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not result:
            return Response(
                {"detail": "No geocoding results found for the given address."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Cache + return
        cache.set(cache_key, result, timeout=getattr(settings, "GEOCODE_CACHE_TTL", 604800))
        return Response(GeocodeOutputSerializer(result).data, status=status.HTTP_200_OK)


class NearbySearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Search for services within a given radius (km) from a point (lat, lng).
        Optional filter by service type.
        """
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        radius_km = request.data.get("radius_km", 5)
        service_type = request.data.get("type")  # optional
        query = request.data.get("query") or (
            f"Nearby {service_type} services within {radius_km}km"
            if service_type
            else f"Nearby services within {radius_km}km"
        )

        if lat is None or lng is None:
            return Response({"detail": "lat and lng are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert inputs to floats
        try:
            lat = float(lat)
            lng = float(lng)
            radius_km = float(radius_km)
        except ValueError:
            return Response(
                {"detail": "lat, lng, and radius_km must be numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Base queryset
        services = Service.objects.all()
        if service_type:
            services = services.filter(type__iexact=service_type)

        # Haversine formula in ORM
        services = services.annotate(
            distance_km=6371
            * ACos(
                Cos(Radians(lat))
                * Cos(Radians(F("lat")))
                * Cos(Radians(F("lng")) - Radians(lng))
                + Sin(Radians(lat)) * Sin(Radians(F("lat")))
            )
        ).filter(distance_km__lte=radius_km).order_by("distance_km")

        # Save search history
        history = SearchHistory.objects.create(
            user=request.user,
            query=query,
            lat=lat,
            lng=lng,
            radius_km=radius_km,
        )

        # Save results
        results = []
        for service in services:
            result = SearchResult.objects.create(
                search=history, service=service, distance_km=service.distance_km
            )
            results.append(result)

        serializer = SearchHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchHistoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = SearchHistory.objects.filter(user=request.user).order_by("-created_at")
        serializer = SearchHistorySerializer(history, many=True)
        return Response(serializer.data)


class SearchHistoryDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            history = SearchHistory.objects.get(pk=pk, user=request.user)
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SearchHistory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)