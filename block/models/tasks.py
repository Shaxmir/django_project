from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.urls import reverse


class Tasks(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    description = models.CharField(max_length=500, validators=[MinLengthValidator(5)])
    is_completed = models.BooleanField(default=False)
    due_data = models.DateTimeField(auto_now_add=True)

    #Проверка на количество символов
    def clean(self):
        super().clean()
        if len(self.title) > 200:
            raise ValidationError({'title' : 'Заголовок превышает допустимое количество символов (200)'})
        elif len(self.title) < 5:
            raise ValidationError({'title' : 'Заголовок не заполнен или количество символов меньше 5'})

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'page': 'tasks', 'id': self.id})


