from django.contrib import admin
from .models import Route, RouteService

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "origin_lat",
        "origin_lng",
        "dest_lat",
        "dest_lng",
        "distance_km",
        "duration_min",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("user__email",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(RouteService)
class RouteServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "route", "service", "distance_km")
    list_filter = ("route", "service")
    search_fields = ("service__name", "route__user__email")
    ordering = ("-id",)
