# Generated by Django 5.1.3 on 2024-11-30 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0011_remove_post_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=1024, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
