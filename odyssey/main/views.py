from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JourneyInformationForm
from .models import JourneyInformation, Itinerary, Activity
from .utils import cities
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    if request.method == 'POST':
        form = JourneyInformationForm(request.POST)
        
        if form.is_valid():
            instance = form.save()
            return redirect('result', pk=instance.pk)
        else:
            print(form.errors)
    else:
        form = JourneyInformationForm()  


    activities = Activity.objects.all()
    unique_cities = set()
    filtered_activities = []  

    for activity in activities:
        if activity.city not in unique_cities:
            unique_cities.add(activity.city)
            filtered_activities.append(activity)
    
    return render(request, "home.html", {'form': form, 'activities': filtered_activities})

def result(request, pk):

    journey = get_object_or_404(JourneyInformation, pk=pk)

    return render(request, "result.html", {'journey': journey})

# def result(request, city, budget):
#     return render(request, "result.html", {'city': city, 'budget': budget})

def profile(request):
    if  request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return redirect('login')
    
def calendar(request):
    if  request.user.is_authenticated:
        return render(request, "calendar.html")
    else:
        return redirect('login')

def autocomplete_cities(request):
    query = request.GET.get('term', '').lower()
    results = [city for city in cities if query in city.lower()][:5]
    return JsonResponse(results, safe=False)

@csrf_exempt
def add_itinerary(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            new_itinerary = Itinerary.objects.create(
                user_id=data["user_id"],
                activity_ids=data["activity_ids"],
                city=data["city"],
                cost=data["cost"],
                departure=data["departure"],
                arrival=data["arrival"]
            )

            return JsonResponse({"message": "Row added successfully!", "id": new_itinerary.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

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