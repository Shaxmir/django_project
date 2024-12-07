from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='message')
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(default=timezone.now)

