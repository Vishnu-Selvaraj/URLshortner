from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Urlshortner(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)
    original_url = models.URLField()
    short_url = models.CharField(max_length=50,unique=True)
    time = models.TimeField(auto_now_add=True)
