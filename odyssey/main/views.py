from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JourneyInformationForm, ProfileUpdateForm
from .models import JourneyInformation, Itinerary, Activity
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from PIL import Image
import os
import json
from django.conf import settings


def home(request):
    # Handles the home page form, validating the input
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

# Function to resize the images used for profile images to avoid errors 
def resize_image(image_path):
    img = Image.open(image_path)
    width, height = img.size

    min_side = min(width, height)
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2

    img = img.crop((left, top, right, bottom))
    img = img.resize((300, 300))
    img.save(image_path)

def profile(request):
    months = {
        'January': 'January',
        'February': 'February',
        'March': 'March',
        'April': 'April',
        'May': 'May',
        'June': 'June',
        'July': 'July',
        'August': 'August',
        'September': 'September',
        'October': 'October',
        'November': 'November',
        'December': 'December',
    }

    itineraries = Itinerary.objects.filter(user_id=request.user.id)

    # Handles the profile photo update form
    if  request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                profile = Profile.objects.get(user=request.user)
                profile.image = form.cleaned_data["image"]
                profile.save()

                image_path = os.path.join(settings.MEDIA_ROOT, str(profile.image))
                resize_image(image_path)
                return redirect('profile')
        else:
            form = ProfileUpdateForm(instance=request.user.profile)
            return render(request, "profile.html", {'months': months, 'user_itineraries': itineraries, 'form': form})
    else:
        return redirect('login')

@csrf_exempt
def add_itinerary(request):
    # Adds the itinerary based on the user input
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            new_itinerary = Itinerary.objects.create(
                user_id=data["user_id"],
                activity_ids=data["activity_ids"],
                city=data["city"],
                country=data["country"],
                cost=data["cost"],
                departure=data["departure"],
                arrival=data["arrival"]
            )

            return JsonResponse({"message": "Row added successfully!", "id": new_itinerary.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@csrf_exempt
def remove_itinerary(request, itinerary_id):
    # Removes the itinerary based on user input
    if request.method == "POST":
        row = get_object_or_404(Itinerary, id=itinerary_id)
        row.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def get_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)

    # Gets the activity details and returns them
    activity_ids = itinerary.activity_ids
    itinerary_data = {}
    for activity_id in activity_ids:
        activity = get_object_or_404(Activity, image=activity_id)
        activity_data = {
            "city": activity.city,
            "title": activity.title,
            "image": activity.image,
            "price": activity.price,
            "desc": activity.short_desc
        }

        itinerary_data[activity.image] = activity_data

    return JsonResponse(itinerary_data)

def custom_login(request):
    # Validates the login input
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "registration/login.html")

def custom_register(request):
    # Validates the registration input, creates the account if valid data inputted
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if ('@' not in email) or ('.' not in email):
            messages.error(request, "Invalid email")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("home")

    return render(request, "registration/register.html")

# Logs the user out
def logout_view(request):
    logout(request)
    return redirect('home')