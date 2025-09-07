from django.urls import path
from .views import (
    GeocodeView,
    NearbySearchView,
    SearchHistoryListView,
    SearchHistoryDeleteView,
)

urlpatterns = [
    path("geocode/", GeocodeView.as_view(), name="geocode"),
    path("nearby/", NearbySearchView.as_view(), name="nearby"),
    path("history/", SearchHistoryListView.as_view(), name="history"),
    path("history/<int:pk>/", SearchHistoryDeleteView.as_view(), name="delete-history"),
]
