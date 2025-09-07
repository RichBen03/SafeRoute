from django.urls import path
from .views import RouteCreateView, RouteListView, RouteDetailView

urlpatterns = [
    path("create/", RouteCreateView.as_view(), name="create-route"),
    path("", RouteListView.as_view(), name="list-routes"),
    path("<int:pk>/", RouteDetailView.as_view(), name="route-detail"),
]
