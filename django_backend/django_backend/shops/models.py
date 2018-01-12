from django.utils import timezone

from mongoengine import fields, Document, ImproperlyConfigured
import mongoengine
from django_backend.restauth.models import User
# Create your models here.

class Shop(Document):
    name = fields.StringField()
    picture = fields.URLField()
    email = fields.EmailField()
    city = fields.StringField()
    location = fields.PointField()
    
    def __str__(self):
        return self.name

class FavoriteShop(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    shop = fields.ReferenceField(Shop, reverse_delete_rule=mongoengine.CASCADE)
    created_at = fields.DateTimeField(auto_now = True, default=timezone.now)
    location = fields.PointField()

class DislikeShop(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    shop = fields.ReferenceField(Shop, reverse_delete_rule=mongoengine.CASCADE)
    created_at = fields.DateTimeField(auto_now = True, default=timezone.now)
    