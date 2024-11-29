from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

class Users(models.Model):
    login = models.CharField(min_length=4,max_length=20,help_text='Логин минимум сим. 4 максимум 20')
    password = models.CharField(min_length=6,help_text='Пароль. Минимум символов 6')
    age = models.IntegerField(validators=[MinLengthValidator(4)],help_text='Возраст. Минимум 3х значное число')
    reg_data = models.DateField(auto_now_add=True,help_text='Дата регистрации(я надеюсь)')
    email = models.EmailField(unique=True,help_text='Эл. почта')
    avatar = models.ImageField(upload_to='users/ava/',help_text='Попробуем загрузить аватар для пользователя')