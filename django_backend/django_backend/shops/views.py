from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse
from django.utils import timezone

from rest_framework import views, mixins, permissions, exceptions, status, serializers
from rest_framework.response import Response
from rest_framework import parsers, renderers
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import NearbyShopSerializer, DislikeShopSerializer, FavoriteShopSerilizer
from .models import Shop, FavoriteShop, DislikeShop

from django_backend.restauth.models import User
from django_backend.restauth.authentication import TokenAuthentication
from mongoengine.errors import DoesNotExist

import os
from bson import ObjectId

# a function that validate data from query_params 
# it checks if latitude and longitude are valid inputs
def validate_location(data):
    # order query results
    if 'lat' in data and 'lng' in data :
        # coordinates needs to be validated and typed 
        lat = data["lat"]
        lng = data["lng"]
        
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return []
            
        if -90<=lat and lat<=90 and -180 <=lng and lng<= 180:
            return [lat, lng] 
            
    return []

class MyPaginationClass(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
class NearbyShopView(ListAPIView):
    # This view takes as input the coordinates of the user
    # and outputs a list of shops ordered by how near the 
    # shop is to the input coordinates
    # It requires authentication from the user
    
    # The resulting list must not include diliked shops (> 2hours)
    # It must inlude an additional attributes that states whether
    # the user has already added the shop as a favorite or not.
    
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = NearbyShopSerializer
    pagination_class = MyPaginationClass
    
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

        result = Shop.objects.filter(id__nin=disliked_shops_2h)
        
        location = validate_location(self.request.query_params)
        if location:
            result = result.filter(location__near=location)
        
        return result

"""
    The dislike shop view handles post requests with the shop id as input
    paramater. If the shop is in the favorite shop list, it is deleted from
    it then added to the list of disliked shops.
"""
class DislikeShopView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = DislikeShopSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response("Shop disliked successfully.", status=status.HTTP_201_CREATED)
        
"""
    This view handles three different kind of requests.
    It servers a get request, taking into account the user's auth token,
    it then returns the list of favorite shops.
    It serves two post requests:
        (1) POST: Adds a shop into the list of favorite shops of a user.
        (2) POST: removes a shop from the list of favorite shops.
    
"""
class FavoriteShopView(mixins.DestroyModelMixin,
                        mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = FavoriteShopSerilizer
    pagination_class = MyPaginationClass
    
    # we need to override this function to serve the delete mixin the right
    # shop object that was requested by the user.
    
    def get_object(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        return serializer.get_object()
    
    def get_queryset(self):
        location = validate_location(self.request.query_params)
        # If the query parameter about the user's location is included, sort 
        # the list of shops according to the nearest one.
        if location:
            subQuery = FavoriteShop.objects(user=self.request.user, location__near=location)
        else:
            subQuery = FavoriteShop.objects(user=self.request.user)
            
        results = [favorite_shop.shop for favorite_shop in subQuery]
        
        return results
 
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NearbyShopSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NearbyShopSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        