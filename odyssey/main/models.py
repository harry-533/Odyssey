from django.db import models

class JourneyInformation(models.Model):
    destination = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.
