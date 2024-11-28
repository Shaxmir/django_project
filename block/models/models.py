from django.db import models

class Users(models.Model):
    login = models.CharField(min_length=4,max_length=20)#Логин минимум сим. 4 максимум 20
    password = models.CharField(min_length=6)#Пароль. Минимум символов 6
    age = models.IntegerField(max_length=3)#Возраст. Минимум 3х значное число
    reg_data = models.DateField(auto_now_add=True)#Дата регистрации(я надеюсь)
    email = models.EmailField(unique=True)#Эл. почта
    avatar = models.ImageField(upload_to='users/ava/')#Попробуем загрузить аватар для пользователя