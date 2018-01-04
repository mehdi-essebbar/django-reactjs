from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _



class ShopsConfig(AppConfig):
    name = 'django_backend.shops'
    verbose_name = _('shops')
    
    def ready(self):
        pass