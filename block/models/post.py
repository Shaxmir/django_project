from audioop import reverse
from django.db import models
from django.core.validators import MinLengthValidator

class Post(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5, message='Меньше 5 символов')])
    content = models.TextField(max_length=1024, validators=[MinLengthValidator(5, message='Меньше 5 символов')])
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата при создании')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата изменении')


    def get_absolute_url(self):
        return reverse('post', kwargs={'page': 'posts', 'id': self.id})
