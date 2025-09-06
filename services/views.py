from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer


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
