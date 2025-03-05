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

# Create your models here.
