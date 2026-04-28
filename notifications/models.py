from django.db import models
from accounts.models import User
import uuid

# Create your models here.

class Notification(models.Model):
    notification_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_read = models.BooleanField(default=False)