from django.contrib import admin
from .models import Service

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "address", "latitude", "longitude", "contact_number", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("name", "address", "contact_number")
    ordering = ("-created_at",)
