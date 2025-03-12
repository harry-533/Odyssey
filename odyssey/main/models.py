from django.db import models
from django.core.validators import RegexValidator

class JourneyInformation(models.Model):
    letter_and_space = RegexValidator('^[A-Za-z ]+$', 'Please only enter letters.')
    destination = models.CharField(max_length=50, validators=[letter_and_space])
    budget = models.IntegerField(default=0)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"{self.id} | {self.destination} with a budget of {self.budget}"

class Activity(models.Model):
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64, blank=True)
    image = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=64)
    price = models.CharField(max_length=8)
    desc = models.CharField(max_length=256)
    short_desc = models.CharField(max_length=64)
    category = models.CharField(max_length=16)
    group_size = models.CharField(max_length=16)
    age = models.CharField(max_length=16)
    duration = models.CharField(max_length=16)
    popularity = models.CharField(max_length=16)
    accessibility = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id} | {self.city} - {self.title}"
    
class Itinerary(models.Model):
    user_id = models.IntegerField(default=0)
    activity_ids = models.JSONField(default=list)
    location = models.CharField(max_length=64)
    cost = models.CharField(max_length=16)
    departure = models.CharField(max_length=16)
    arrival = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.id} | {self.city} - £{self.cost}"
