from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from .models import Route, RouteService
from services.models import Service
from .serializers import RouteSerializer
from .utils import get_route, haversine_distance, closest_distance_to_route


class RouteCreateView(APIView):
    """
    Creates a route from origin to destination, stores it in DB, 
    and attaches nearby services.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        origin = request.data.get("origin")        # expected: [lat, lng]
        destination = request.data.get("destination")  # expected: [lat, lng]
        radius_km = float(request.data.get("radius_km", 1))  # distance to check services

        # Validate coordinates
        if not origin or not destination or len(origin) != 2 or len(destination) != 2:
            return Response(
                {"detail": "Origin and destination must be arrays of [lat, lng]."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            origin = tuple(map(float, origin))
            destination = tuple(map(float, destination))
        except ValueError:
            return Response(
                {"detail": "Coordinates must be numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (0 < radius_km <= 10):
            return Response(
                {"detail": "radius_km must be between 0.1 and 10 km."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get route from ORS or cache
        route_data = get_route(origin, destination)

        with transaction.atomic():
            # Store route in DB
            route_instance = Route.objects.create(
                user=request.user,
                origin_lat=origin[0],
                origin_lng=origin[1],
                dest_lat=destination[0],
                dest_lng=destination[1],
                distance_km=route_data["distance_m"] / 1000,
                duration_min=route_data["duration_s"] / 60,
                geometry=route_data["geometry"],
                steps=route_data["steps"],
            )

            # Attach nearby services along the route
            for service in Service.objects.all():
                distance_to_route = closest_distance_to_route(
                    route_data["geometry"], (service.lat, service.lng)
                )
                if distance_to_route <= radius_km:
                    RouteService.objects.create(
                        route=route_instance,
                        service=service,
                        distance_km=distance_to_route
                    )

        serializer = RouteSerializer(route_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RouteListView(APIView):
    """
    Lists all routes created by the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        routes = Route.objects.filter(user=request.user).order_by("-created_at")
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)


class RouteDetailView(APIView):
    """
    Returns details of a specific route, including nearby services.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            route = Route.objects.get(pk=pk, user=request.user)
        except Route.DoesNotExist:
            return Response({"detail": "Route not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RouteSerializer(route)
        return Response(serializer.data)
