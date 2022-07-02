from django import urls
from django.urls import path
from messenger import *
from .views import *


urlpatterns = [
    path('mensajes', mensajes.as_view(), name='mensajes'),
]
