# Generated by Django 5.1.6 on 2025-03-11 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_itinerary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journeyinformation',
            name='budget',
            field=models.IntegerField(default=0),
        ),
    ]
