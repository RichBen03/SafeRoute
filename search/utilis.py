import re
import requests
from django.conf import settings


def normalize_address(address: str) -> str:
    # lowercase + collapse whitespace for consistent cache key
    return re.sub(r"\s+", " ", address.strip().lower())


def geocode_nominatim(address: str) -> dict | None:
    """
    Calls Nominatim to geocode an address.
    Returns {lat, lng, display_name} or None if no results.
    Raises requests.HTTPError on non-2xx responses.
    """
    base = settings.NOMINATIM_BASE_URL.rstrip("/")
    url = f"{base}/search"
    params = {"q": address, "format": "json", "addressdetails": 1, "limit": 1}
    headers = {
        "User-Agent": f"SafeRouteAPI/1.0 ({settings.NOMINATIM_CONTACT_EMAIL})"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        return None

    top = data[0]
    return {
        "lat": float(top["lat"]),
        "lng": float(top["lon"]),
        "display_name": top.get("display_name", address),
    }