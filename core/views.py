from django.shortcuts import render
import datetime

def home(request):
    return render(request, "core/home.html", {"year": datetime.datetime.now().year})

def about(request):
    return render(request, "core/about.html", {"year": datetime.datetime.now().year})