from django.http import HttpResponse as hr
from django.shortcuts import render

def start(request):
    return render(request, 'start.html')