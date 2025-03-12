from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('result/<str:city>/<str:budget>', views.result, name='result'),
    path('profile/', views.profile, name='profile'),
    path('calendar/', views.calendar, name='calendar'),
    path('autocomplete/', views.autocomplete_cities, name='autocomplete_cities'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add-row/', views.add_itinerary, name="add_row"),
    path('result/<int:pk>/', views.result, name='result')
]