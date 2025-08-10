from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_entries')
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_favorite = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_expiry = models.DateTimeField(blank=True, null=True)
    is_qr_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.password} - {self.user.username}"
