from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Home")

def result_page(request):
    return HttpResponse("Result")