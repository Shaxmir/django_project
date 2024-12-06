from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Poll(models.Model):
    title = models.CharField(max_length=50, validators=[MinLengthValidator(10)])
    description = models.TextField(max_length=500, validators=[MinLengthValidator(50)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('poll', kwargs={'page': 'polls', 'id' : self.id})

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    votes = models.IntegerField(default=0)

class User_poll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='user_poll')
    ip_address = models.GenericIPAddressField()