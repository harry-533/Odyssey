from django.contrib import admin
from .models import JourneyInformation, Activity, Itinerary

admin.site.register(JourneyInformation)
admin.site.register(Activity)
admin.site.register(Itinerary)