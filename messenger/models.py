from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='hilos')
    

class Mensaje(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sent_at']
    
