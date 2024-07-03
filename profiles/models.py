from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', default='./DEFAULTS/profile_default')
    
  
