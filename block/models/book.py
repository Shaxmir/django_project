from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db.models import IntegerField, PositiveIntegerField, DecimalField
from django.forms import FloatField


class Book(models.Model):
    title = models.CharField(max_length=150, validators=[MinLengthValidator(10)])
    author = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    published_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    stock = models.IntegerField()