from django.contrib import admin
from .models import Mensaje, Thread

# Register your models here.
admin.site.register(Mensaje)
admin.site.register(Thread)