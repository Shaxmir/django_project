from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

class Tasks(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    description = models.CharField(max_length=500, validators=[MinLengthValidator(5)])
    is_completed = models.BooleanField(default=False)
    due_data = models.DateTimeField(auto_now_add=True)