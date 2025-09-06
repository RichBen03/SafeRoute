from django.contrib import admin
from .models import Service

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "address", "lat", "lng", "contact_info", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("name", "address", "contact_info")
    ordering = ("-created_at",)
