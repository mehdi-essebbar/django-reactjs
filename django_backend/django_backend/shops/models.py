from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Shop(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to='shops')
    
    def __str__(self):
        return self.name
        
class UserFavoriteShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    
        
class UserDislikedShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    