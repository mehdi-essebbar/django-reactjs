from .models import Shop, UserFavoriteShop
from .serializers import ShopSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ShopView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
class ShopsView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
        
class FavoriteShopsView(APIView):
    
    def get(self, request, user, format=None):
        favorite_shops = UserFavoriteShop.objects.filter(user_id=user)
        shops = [result.shop for result in favorite_shops]
        serialize = ShopSerializer(shops, many=True)
        return Response(serialize.data)
        