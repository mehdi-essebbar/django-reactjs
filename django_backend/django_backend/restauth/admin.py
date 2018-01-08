from django_mongoengine import mongo_admin as admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdminModel(admin.DocumentAdmin):
    pass