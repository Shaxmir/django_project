# Generated by Django 5.1.3 on 2024-11-30 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0006_alter_book_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(5)])),
                ('content', models.TextField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата при создании')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Дата изменении')),
            ],
        ),
    ]
