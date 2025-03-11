from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JourneyInformationForm
from .models import JourneyInformation
from .utils import cities
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    if request.method == 'POST':
        form = JourneyInformationForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return redirect('result', pk=instance.pk)
    else:
        form = JourneyInformationForm()  
    
    return render(request, "home.html", {'form': form})

def result(request, city, budget):
    return render(request, "result.html", {'city': city, 'budget': budget})

def autocomplete_cities(request):
    query = request.GET.get('term', '').lower()
    results = [city for city in cities if query in city.lower()][:5]
    return JsonResponse(results, safe=False)

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "registration/login.html")

def custom_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("home")

    return render(request, "registration/register.html")

def logout_view(request):
    logout(request)
    return redirect('home')

# def result(request, pk):

#     journey = get_object_or_404(JourneyInformation, pk=pk)

#     return render(request, "result.html", {'journey': journey})