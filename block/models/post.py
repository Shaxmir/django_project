from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

class Post(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата при создании')
    updated_at = models.DateTimeField(auto_now=True, blank=True, help_text='Дата изменении')