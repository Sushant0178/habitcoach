from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def notifications_home(request):
    return HttpResponse("Welcome to the Notifications Home Page")