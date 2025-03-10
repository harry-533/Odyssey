from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('result/<str:city>/<str:budget>', views.result, name='result'),
    path('autocomplete/', views.autocomplete_cities, name='autocomplete_cities')
    # path('result/<int:pk>/', views.result, name='result')
]