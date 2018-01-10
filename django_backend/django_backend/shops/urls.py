from django.conf.urls import url
from . import views

urlpatterns = [
    # All shop services require authentication
    url(r'^$', views.NearbyShopView.as_view(), name='nearby_shop'), # get
    url(r'^dislike/$', views.DislikeShopView.as_view(), name='dislike_shop'), # create (shop id)
    url(r'^favorite/$', views.FavoriteShopView.as_view(), name='favorite_shop'), # get, create (shop id), delete (shop id)
]
