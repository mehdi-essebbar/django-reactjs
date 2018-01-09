from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import exceptions
from project import settings

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_mongoengine.serializers import DocumentSerializer
from mongoengine import fields
from mongoengine.errors import DoesNotExist

from django_backend.restauth.models import User
from .models import Shop, FavoriteShop, DislikeShop

from bson import ObjectId, errors

import sys


class NearbyShopSerializer(DocumentSerializer):
    shop_id = fields.ObjectIdField(source='id')
    is_favorite = fields.BooleanField(default=False)
    
    class Meta:
        model = Shop
        fields = ('id', 'name', 'email', 'picture', 'city', )
    
class DislikeShopSerializer(serializers.Serializer):
    
    shop_id = serializers.CharField()
    
    def __init__(self, *args, **kwargs):
        super(DislikeShopSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
    
    def validate_shop_id(self, shop_id):
        #Check if the shop id does exist
        try:
            self.shop = Shop.objects.get(id=shop_id)
        except DoesNotExist:
            raise serializers.ValidationError("The given shop id does not exists.")
        
        return shop_id
    
    def save(self):
        dislike = DislikeShop(user=self.user, shop=self.shop)
        dislike.save()
"""
class FavoriteShopSerilizer(DocumentSerializer):
    
    class Meta:
        model= Shop
        fields= '__all__'
    """
    
class FavoriteShopSerilizer(serializers.Serializer):
    id = serializers.CharField()
    
    def __init__(self, *args, **kwargs):
        super(FavoriteShopSerilizer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        
        self.user = getattr(self.request, 'user', None)
    
    def validate_id(self, id):
        
        try:
            ObjectId(id)
        except (TypeError, errors.InvalidId):
            raise serializers.ValidationError("The given shop id is not valid.")
        
        try:
            self.shop = Shop.objects.get(id=id)
        except DoesNotExist:
            raise serializers.ValidationError("The given shop id does not exists.")
        
        return id
        
    def check_favorite_already(self):
        if FavoriteShop.objects.filter(shop=self.shop, user=self.user):
            raise serializers.ValidationError("Shop already in favorite list.")
    
    def get_object(self):
        try:
            shop = FavoriteShop.objects.get(shop=self.shop, user=self.user)
        except DoesNotExist:
            raise serializers.ValidationError("This shop is not in your favorite list.")
            
        return shop
    
    def save(self):
        self.check_favorite_already()
        favorite_shop = FavoriteShop(shop=self.shop, user=self.user)
        favorite_shop.save()
        