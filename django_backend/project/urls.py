from django.conf.urls import include, url
from django.contrib import admin
from django_mongoengine import mongo_admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),

    # This is used for user reset password
    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(mongo_admin.site.urls)),
    url(r'^rest-auth/', include('django_backend.restauth.urls', namespace='rest-auth')),
    url(r'^shops/', include('django_backend.shops.urls', namespace='shop')),
    
    #url(r'^$', index_view, {}, name='index'),
    #url(r'^api/',  include(router.urls)),   
    #url(r'^api/shops/',  include('django_backend.shops.urls')),
]

# let django built-in server serve static and media content
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)