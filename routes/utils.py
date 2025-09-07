import openrouteservice
from django.conf import settings
from math import radians, cos, sin, asin, sqrt
from django.core.cache import cache

# Initialize ORS client
ors_client = openrouteservice.Client(key=settings.ORS_API_KEY)


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Returns distance in km between two points using Haversine formula.
    """
    r = 6371  # Earth radius in km
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lng2 - lng1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * asin(sqrt(a))
    return r * c


def get_route(origin, destination, profile="driving-car"):
    """
    Fetch route from ORS or return cached result.
    origin, destination: (lat, lng) tuples
    Returns dict with geometry, distance_m, duration_s, steps
    """
    cache_key = f"route:{origin[0]}_{origin[1]}_{destination[0]}_{destination[1]}_{profile}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    coords = [(origin[1], origin[0]), (destination[1], destination[0])]  # ORS expects (lng, lat)
    route = ors_client.directions(coordinates=coords, profile=profile, format="geojson")

    feature = route["features"][0]
    summary = feature["properties"]["summary"]
    segments = feature["properties"]["segments"][0]["steps"]
    geometry = feature["geometry"]["coordinates"]

    result = {
        "geometry": geometry,
        "distance_m": summary["distance"],
        "duration_s": summary["duration"],
        "steps": segments,
    }

    # Cache for 24 hours
    cache.set(cache_key, result, timeout=86400)
    return result


def closest_distance_to_route(route_coords, point):
    """
    Returns the shortest distance (km) from a point (lat, lng) to a list of route coordinates.
    """
    min_distance = float("inf")
    lat2, lng2 = point
    for coord in route_coords[::5]:  # Downsample every 5 points for efficiency
        lng1, lat1 = coord
        distance = haversine_distance(lat1, lng1, lat2, lng2)
        if distance < min_distance:
            min_distance = distance
    return min_distance
