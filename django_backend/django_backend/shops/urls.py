from django.conf.urls import url
from . import views

urlpatterns = [
    # This is used for user reset password
    url(r'^(?P<id>[0-9]+)', views.ShopView.as_view(), name='shop'),
    url(r'^user/(?P<user>\d+)', views.FavoriteShopsView.as_view(), name='favorite_shops'),
    url(r'^', views.ShopsView.as_view(), name='list_shops'),  
]
