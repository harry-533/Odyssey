from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class JourneyInformation(models.Model):
    letter_and_space = RegexValidator('^[A-Za-z ]+$', 'Please only enter letters.')
    city = models.CharField(max_length=50, validators=[letter_and_space])
    country = models.CharField(max_length=50, validators=[letter_and_space])
    budget = models.IntegerField(default=0)
    date_from = models.DateField()
    date_to = models.DateField()

    def clean(self):
        if self.date_from < now().date():
            raise ValidationError('Please only enter dates in the future')
        if self.date_from > self.date_to:
            raise ValidationError('Please ensure the dates are in the correct order')

    def __str__(self):
        return f"{self.id} | {self.city} with a budget of {self.budget}"

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
    city = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    cost = models.CharField(max_length=16)
    departure = models.CharField(max_length=16)
    arrival = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.id} | {self.city} - £{self.cost}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='default.png')

    def __str__(self):
        return f'{self.user.username} Profile'