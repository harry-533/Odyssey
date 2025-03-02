from django.template import loader
from django.shortcuts import render, redirect
from .models import JourneyInformation

def home(request):
    if request.method == 'POST':
        destination = request.POST.get('destination')
        budget = request.POST.get('budget')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        JourneyInformation.objects.create(
            destination=destination,
            budget=budget,
            date_from=date_from,
            date_to=date_to
        )

        return redirect('result.html')
    
    return render(request, "home.html")

def result(request):
    return render(request, "result.html")