from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    is_completed = models.BooleanField(default=False)
    due_data = models.DateTimeField(default=timezone.now)

    #Проверка на количество символов
    def clean(self):
        super().clean()
        if len(self.title) > 200:
            raise ValidationError({'title' : 'Заголовок превышает допустимое количество символов (200)'})
        elif len(self.title) < 5:
            raise ValidationError({'title' : 'Заголовок не заполнен или количество символов меньше 5'})
        elif len(self.description) < 5 or len(self.description) > 500:
            raise ValidationError({'description' : 'Текста мало или мноха'})

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'page': 'tasks', 'id': self.id})


