from django.contrib import admin
from .models import Shop, UserFavoriteShop, UserDislikedShop

# Register your models here.
@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'picture']

@admin.register(UserFavoriteShop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop', 'created_at']

        