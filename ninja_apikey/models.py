# type: ignore
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class APIKey(models.Model):
    prefix = models.CharField(max_length=8, primary_key=True)
    hashed_key = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    label = models.CharField(max_length=40)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    @property
    def is_valid(self):
        if self.revoked:
            return False

        if not self.expires_at:
            return True  # No expiration

        return self.expires_at >= timezone.now()

    def __str__(self):
        return f"{self.user.username}<{self.prefix}>"
