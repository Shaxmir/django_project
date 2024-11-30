from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator




class Author(models.Model):
    author = models.CharField(max_length=25, validators=[MinLengthValidator(3)])

class Message(models.Model):
    author = models.OneToOneField(Author, on_delete= models.CASCADE, primary_key=True)
    content = models.TextField(max_length=1024, validators=[MinLengthValidator(10)])
    create_at = models.DateTimeField(auto_now_add=True)
