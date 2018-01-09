from django.conf.urls import url
from . import views

urlpatterns = [
    # This is used for user reset password
    #url(r'^(?P<id>[0-9]+)', views.ShopView.as_view(), name='shop'),
    #url(r'^user/(?P<user>\d+)', views.FavoriteShopsView.as_view(), name='favorite_shops'),
    #url(r'^', views.ShopsView.as_view(), name='list_shops'),  
    
    # All shop services require authentication
    url(r'^$', views.NearbyShopView.as_view(), name='nearby_shop'), # get
    url(r'^dislike/$', views.DislikeShopView.as_view(), name='dislike_shop'), # create (shop id)
    url(r'^favorite/$', views.FavoriteShopView.as_view(), name='favorite_shop'), # get, create (shop id), delete (shop id)
    #url(r'^favorite/(?P<id>[a-f\d]{24})$', views.RemoveCreateShopView.as_view(), name='add_remove_favorite_shop'),
]
