import datetime
import binascii
import os

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import mongoengine
from django_mongoengine.mongo_auth.models import AbstractUser
from mongoengine import fields, Document, ImproperlyConfigured


class User(AbstractUser):
    """
    VERSION ISSUES:

    In Mongoengine <= 0.9 there is a mongoengine.django subpackage, which
    implements mongoengine User document and its integration with django
    authentication system.

    In Mongoengine >= 0.10 mongoengine.django was extracted from Mongoengine
    codebase and moved into a separate repository - django-mongoengine. That
    repository contains an AbstractBaseUser class, so that you can just
    inherit your User model from it, instead of copy-pasting the following
    200 lines of boilerplate code from mongoengine.django.auth.User.
    """
    
    #bio = fields.StringField(max_length=1000)
    about = fields.StringField(max_length=1000, blank=True)
    website = fields.URLField(blank=True)
    # For email validation
    email_is_valid = fields.BooleanField(default=False)

@python_2_unicode_compatible
class EmailValidationToken(Document):
    token = fields.StringField(required=True)
    created_at = fields.DateTimeField(auto_now=True, default=timezone.now)
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    
    def __str__(self):
        return self.token

class PasswordResetToken(Document):
    token = fields.StringField(required=True)
    created_at = fields.DateTimeField(auto_now=True, default=timezone.now)
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super(PasswordResetToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    def __str__(self):
        return self.token
 
@python_2_unicode_compatible
class Token(Document):
    """
    This is a mongoengine adaptation of DRF's default Token.

    The default authorization token model.
    """
    key = fields.StringField(required=True)
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    created = fields.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
