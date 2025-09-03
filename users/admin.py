from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Token

# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    # show role and location_preference in admin list
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'location_preference')}),
    )
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at')
    search_fields = ('user__username', 'token')
