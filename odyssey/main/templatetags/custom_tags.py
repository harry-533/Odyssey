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
    
@register.simple_tag
def get_itinerary_activities(activity_ids):
    activities = []
    if type(activity_ids) == list:
        for activity_id in activity_ids:
            activity = Activity.objects.get(image=activity_id)
            activity_dict = {"city": activity.city, "image": activity.image, "title": activity.title,
                             "price": activity.price, "desc": activity.short_desc}
            activities.append(activity_dict)

    return activities

@register.simple_tag
def get_itinerary_image(activity_ids):
    if type(activity_ids) == list:
        activity = Activity.objects.get(image=activity_ids[0])
    return activity

@register.simple_tag
def get_full_month(month):
    if "." in month:
        month = month.split(".")[0]
        match month:
            case "Jan":
                return "January"
            case "Feb":
                return "February"
            case "Aug":
                return "August"
            case "Sep":
                return "September"
            case "Oct":
                return "October"
            case "Nov":
                return "November"
            case "Dec":
                return "December"
            
    return month