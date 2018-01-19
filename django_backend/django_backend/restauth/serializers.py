from django.contrib.auth import authenticate
import django.contrib.auth.password_validation as validators
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.core import exceptions
from project import settings

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_mongoengine.serializers import DocumentSerializer
from mongoengine.fields import ObjectIdField
from mongoengine.errors import DoesNotExist

from .models import User, PasswordResetToken


class AuthTokenSerializer(serializers.Serializer):
    #username = serializers.CharField(label=_("Username"))
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    
    def validate_email(self, email):
        # email validation start by checking if the email address exists in
        # the database.
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise serializers.ValidationError("No user account attached to the provided email.")
        
        self.username = user.username
        return email
        
    def validate(self, attrs):
        #username = attrs.get('username')
        username = self.username
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                
                if not user.email_is_valid:
                    msg = _('User account email not verified.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserSerializer(DocumentSerializer):
    #id = serializers.IntegerField(read_only=False)
    user_id = ObjectIdField(source='id')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'about', 'website')
        read_only_fields = ('email', )
    

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=120,
        min_length=5)
        
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    def validate_username(self, username):
        #TODO better username validation
        regexp = "/^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$/"
        #validate with regexp
        #check if username exists
        usr = User.objects.filter(username=username)
        if usr:
            raise serializers.ValidationError(
                _("A user is already registered with this username."))
        return username

    def validate_email(self, email):
        # Check if a already uses this email
        usr = User.objects.filter(email=email)
        if usr:
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        #TODO better password constraints (length, uppercase, lowercase, special characters, etc)
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        new_user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        new_user.set_password(self.cleaned_data['password1'])
        new_user.save()
        return new_user

    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_constraints': _("Password constraints not respected."),
        }
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        
        return value

    def validate(self, attrs):
        # validate the passwords
        old_pwd = attrs.get('old_password')#getattr(self.request, 'old_password')
        self.validate_old_password(old_pwd)
        
        new_pwd1 = attrs.get('new_password1')
        new_pwd2 = attrs.get('new_password2')
        
        if new_pwd1 == new_pwd2:
            # validate password constraints : length and characters user
            if not self.validate_password_constraints(new_pwd1):
                # save the new password
                raise serializers.ValidationError(self.error_messages['password_constraints'])
        else:
            raise serializers.ValidationError(self.error_messages['password_mismatch'])
        
        self.new_pwd = new_pwd1
        
        return attrs
    
    def validate_password_constraints(self, pwd):
        if len(pwd) < 8:
            return False
        
        return True
        
    def save(self):
        # save the new password in the database
        self.user.set_password(self.new_pwd)
        self.user.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(self.request, self.user)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(PasswordResetSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
    
    def validate_email(self, email):
        try:
            usr = User.objects.get(email=email)
        except DoesNotExist:
            raise serializers.ValidationError("No user account found associated with this email '"+email+"'")
            
        if not usr.is_active:
            raise serializers.ValidationError("The user account associated is deleted.")
        elif not usr.email_is_valid:
            raise serializers.ValidationError("The user account email is not verified yet.")
    
        self.user = usr
        self.email = email
        return email
        
    def save(self):
        if not self.create_and_send_token():
            raise serializers.ValidationError("We couldn't send you a password reset email. Please, contact administration.")
    
    def create_and_send_token(self):
        msg = """As you request to reset your password, we have sent you this 
                 email. Please browse the link bellow to proceed to reset your password."""
        
        # create a new token
        token = PasswordResetToken(user=self.user)
        token.save()
        print (token)
        url= self.request.META['HTTP_ORIGIN']
        msg +="\n\n" + url +"/reset/"+ token.token
        
        n = send_mail(
            'Reset password',
            msg,
            settings.ADMIN_EMAIL,
            [self.email],
            fail_silently=False,
            )
        
        # Email sent successfully
        if n>0:
            return True
        
        token.delete()
        return False
 
class ConfirmPasswordSerializer(serializers.Serializer):
    
    token = serializers.CharField()
    new_password1 = serializers.CharField(min_length=8, max_length=128)
    new_password2 = serializers.CharField(min_length=8, max_length=128)
    
    def validate_token(self, token):
        # check if token exists in the database
        
        try:
            valid = PasswordResetToken.objects.get(token=token)
        except DoesNotExist:
            
            msg = {"detail": _("Your token is not valid.")} 
            raise serializers.ValidationError(msg)
        
        #print (valid)
        
        #Check if the token has expired
        expiration = timezone.now() - valid.created_at
        
        # If the reset password email was sent more than 15 mins ago, then it expired
        if expiration.total_seconds()/60 > 15:
            valid.delete()
            msg = {"detail": _("Expired token. Go reset your password again.")} 
            raise serializers.ValidationError(msg)
        
        # remove the token and validate it
        self.user = valid.user
        self.token = valid
        
        return token
    
    def validate(self, attrs):
        pwd1 = attrs.get('new_password1')
        pwd2 = attrs.get('new_password2')
        
        if pwd1 != pwd2:
            msg = {'detail':'Passwords mismatch.'}
            raise serializers.ValidationError(msg)
        
        # check if password respect constraints
        if not self.pwd_constraints(pwd1):
            msg = {'detail':'The password does not respect security constraints.'}
            raise serializers.ValidationError(msg)
        
        self.pwd = pwd1
        
        return attrs
        
    def pwd_constraints(self, pwd):
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=pwd, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
         
        #Add some security constraints such a regexp validation (criteria: cap letters, special chars, numbers, etc)
        return True
    
    def save(self):
        # save the new password
        self.user.set_password(self.pwd)
        self.token.delete()
        
        
        