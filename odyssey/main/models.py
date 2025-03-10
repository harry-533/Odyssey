from django.db import models
from django.core.validators import RegexValidator

class JourneyInformation(models.Model):

    letter_and_space = RegexValidator('^[A-Za-z ]+$', 'Please only enter letters.')
    destination = models.CharField(max_length=50, validators=[letter_and_space])
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"{self.id} : {self.destination} with a budget of {self.budget}"

class Activity(models.Model):
    activity_city = models.CharField(max_length=64)
    activity_image = models.CharField(max_length=64, blank=True)
    activity_title = models.CharField(max_length=64)
    activity_price = models.CharField(max_length=8)
    activity_desc = models.CharField(max_length=256)
    activity_short_desc = models.CharField(max_length=64)
    activity_type = models.CharField(max_length=16)
    activity_group_size = models.CharField(max_length=16)
    activity_age = models.CharField(max_length=16)
    activity_duration = models.CharField(max_length=16)
    activity_popularity = models.CharField(max_length=16)
    activity_accessibility = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.activity_city} - {self.activity_title}"
