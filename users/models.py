from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = (
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
    )

    # Inherits: username, first_name, last_name, email, password, is_staff, is_active, date_joined
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    location_preference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
        

class Token(models.Model):
    user = models.ForeignKey("users.User", related_name="tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=500, help_text="Refresh token or opaque token")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return self.expires_at is not None and timezone.now() >= self.expires_at

    def __str__(self):
        return f"Token(user={self.user_id}, created={self.created_at})"
