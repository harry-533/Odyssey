from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JourneyInformationForm
from .models import JourneyInformation


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

# def result(request, pk):

#     journey = get_object_or_404(JourneyInformation, pk=pk)

#     return render(request, "result.html", {'journey': journey})
