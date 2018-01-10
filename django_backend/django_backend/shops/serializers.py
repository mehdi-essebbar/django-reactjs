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
    #shop_id = fields.ObjectIdField(source='id')
    is_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = Shop
        fields = ('id', 'name', 'email', 'picture', 'city', 'is_favorite' )
    
    def __init__(self, *args, **kwargs):
        super(NearbyShopSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
    
    def get_is_favorite(self, obj):
        try:
            FavoriteShop.objects.get(user=self.user, shop=obj)
        except DoesNotExist:
            return 0
            
        return 1
        

        
class DislikeShopSerializer(serializers.Serializer):
    
    id = serializers.CharField()
    
    def __init__(self, *args, **kwargs):
        super(DislikeShopSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
    
    def validate_id(self, id):
        #Check if the shop id does exist
        try:
            self.shop = Shop.objects.get(id=id)
        except DoesNotExist:
            raise serializers.ValidationError("The given shop id does not exists.")
        
        return id
    
    def save(self):
        # if the shop was in the favorite list, take it off
        try:
            noMoreFave = FavoriteShop.objects.get(user=self.user, shop=self.shop)
            noMoreFave.delete()
        except DoesNotExist:
            # do nothing
            pass
        
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
        