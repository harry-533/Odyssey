from django import template
from main.models import *

register = template.Library()

@register.simple_tag
def get_activities():
    return Activity.objects.all()

@register.simple_tag
def get_itineraries():
    return Itinerary.objects.all()

@register.simple_tag
def get_journey(pk):
    try:
        journey = JourneyInformation.objects.get(pk=pk)
        return journey
    except JourneyInformation.DoesNotExist:
        return None