# Generated by Django 4.2.2 on 2023-10-07 22:23

import datetime

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0006_alter_experience_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 10, 7))]),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 10, 7))]),
        ),
    ]
