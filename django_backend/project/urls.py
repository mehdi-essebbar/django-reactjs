from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),

    # This is used for user reset password
    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^rest-auth/', include('django_backend.restauth.urls', namespace='rest-auth')),
    #url(r'^api/',  include(router.urls)),   
    #url(r'^api/shops/',  include('django_backend.shops.urls')),
]
