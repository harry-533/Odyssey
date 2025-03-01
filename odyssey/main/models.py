from django.db import models

class JourneyInformation(models.Model):
    destination = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"{self.id} : {self.destination} with a budget of {self.budget}"

# Create your models here.
