from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JourneyInformationForm
from .models import JourneyInformation
# from .utils import cities


def home(request):
    if request.method == 'POST':
        form = JourneyInformationForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('result', pk=instance.pk)
    else:
        form = JourneyInformationForm()  
    
    return render(request, "home.html", {'form': form})

def result(request):
    return render(request, "result.html")

def autocomplete_cities(request):
    query = request.GET.get('term', '').lower()
    results = [city for city in cities if query in city.lower()][:5]
    return JsonResponse(results, safe=False)


# def result(request, pk):

#     journey = get_object_or_404(JourneyInformation, pk=pk)

#     return render(request, "result.html", {'journey': journey})