from django.shortcuts import render
from django.views.generic.list import ListView
from requests import request
from messenger.models import Mensaje, Thread
from django.utils import timezone

# Create your views here.
class mensajes(ListView):
    
    model = Thread
    
    queryset = Thread.objects.filter()

    
    template_name = "messenger/mensajes.html"
