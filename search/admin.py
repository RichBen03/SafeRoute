from django.contrib import admin
from .models import SearchHistory, SearchResult

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "query", "lat", "lng", "radius_km", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "query")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ("id", "search", "service", "distance_km")
    list_filter = ("search", "service")
    search_fields = ("service__name", "search__user__email")
    ordering = ("-id",)
