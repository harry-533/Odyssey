# Generated by Django 5.1.6 on 2025-03-12 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_itinerary_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journeyinformation',
            old_name='destination',
            new_name='city',
        ),
        migrations.AddField(
            model_name='journeyinformation',
            name='country',
            field=models.CharField(default=1, max_length=50, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', 'Please only enter letters.')]),
            preserve_default=False,
        ),
    ]
