from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('result/<int:pk>/', views.result, name='result')
]