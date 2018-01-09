from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse
from django.utils import timezone

from rest_framework import views, mixins, permissions, exceptions, status, serializers
from rest_framework.response import Response
from rest_framework import parsers, renderers
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView

from .serializers import NearbyShopSerializer, DislikeShopSerializer, FavoriteShopSerilizer#, RemoveCreateFavoriteShopSerializer
from .models import Shop, FavoriteShop, DislikeShop

from django_backend.restauth.models import User
from django_backend.restauth.authentication import TokenAuthentication
from mongoengine.errors import DoesNotExist

import os
from bson import ObjectId
 


class NearbyShopView(ListAPIView):
    # This view takes as input the coordinates of the user
    # and outputs a list of shops ordered by how near the 
    # shop is to the input coordinates
    # It requires authentication from the user
    
    # The resulting list must not include diliked shops (> 2hours)
    # It must inlude an additional attributes that states whether
    # the user has alreaded added the shop as a favorite or not.
    
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = NearbyShopSerializer
    
    def get_queryset(self):
        # First, lets filter the result by taking off disliked shops
        disliked_shops = DislikeShop.objects.filter(user=self.request.user)
        # only those disliked less than two hours ago
        
        disliked_shops_2h = []
        for disliked_shop in disliked_shops:
            time_diff = timezone.now() - disliked_shop.created_at
            time_diff_minutes = time_diff.total_seconds()/60
            if time_diff_minutes < 120:
                disliked_shops_2h.append(str(disliked_shop.shop.id))

        result = Shop.objects.filter(id__nin=disliked_shops_2h).limit(5)
        # Add the attribute is_favorite to the results
        
        return result
 
class DislikeShopView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = DislikeShopSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response("Shop disliked successfully.", status=status.HTTP_201_CREATED)
        
class FavoriteShopView(mixins.DestroyModelMixin,
                        mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = FavoriteShopSerilizer
    
    def get_object(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        return serializer.get_object()
    
    def get_queryset(self):
        return [favorite_shop.shop for favorite_shop in FavoriteShop.objects(user=self.request.user)]
 
    def get(self, request, *args, **kwargs):
        
        serializer = NearbyShopSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
        
        #return self.list(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
"""
class RemoveCreateShopView(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = RemoveCreateFavoriteShopSerializer
    
    def get_object(self):
        serializer = self.get_serializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        
        return serializer.get_object()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        """