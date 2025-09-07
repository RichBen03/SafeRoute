from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet
from .views import GeocodeView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
    path("search/geocode/", GeocodeView.as_view(), name="search-geocode"),
]
