from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.reverse import reverse

from rest_framework import views, mixins, permissions, exceptions, status
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework import parsers, renderers
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

from .serializers import *
from .models import User, Token, EmailValidationToken
from .authentication import TokenAuthentication
from mongoengine.errors import DoesNotExist

import binascii, os, datetime, pytz
from project import settings

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Read-only User endpoint
    """
    permission_classes = (permissions.IsAuthenticated, )  # IsAdminUser?
    authentication_classes = (TokenAuthentication, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
        
class UserView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )  # IsAdminUser?
    authentication_classes = (TokenAuthentication, )
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
        
    def get_queryset(self):
        return User.objects.none()
    
    def put(self, request, *args, **kwargs):
        print (request.data)
        return self.partial_update(request, *args, **kwargs)
    
class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})

class SignUpView(GenericAPIView):
    # This view is for the creation of a new User account
    # It create the user according to its model User (unique username and email)
    # It create an account which needs to be validated by email (send mail
    # to confirm the user email)
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        #result = self.create(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request)
        
        (token, validToken) = self.create_token(User.objects.get(username=serializer.validated_data['username']))
        sent = self.send_validation_email(serializer.validated_data['email'], token)
        
        if not sent:
            msg = {"detail": _("Invalid email address.")}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        
        validToken.save()
        msg = {"detail": _("Go check your email address.")} 
        return Response(msg, status=status.HTTP_201_CREATED)
        # Send email for email validation
     
    def send_validation_email(self, address_email, token):
        msg = """This is the validation email. To consume our services
                and be able to login to our plateform you need to 
                validate your email address by clicking on the link bellow.
                Thank you!"""
        url= self.request.get_host()
        msg +="\n\n" + url +reverse("rest-auth:verify_email")+"?token="+ token
        
        n = send_mail(
            'Validation Email to Signup',
            msg,
            settings.ADMIN_EMAIL,
            [address_email],
            fail_silently=False,
            )
        
        if n>0:
            return True
        
        return False
        
    def create_token(self, user):
        #token = secrets.token_urlsafe(32)
        token = binascii.hexlify(os.urandom(32)).decode()
        validToken = EmailValidationToken(token=token, user=user)
        return (token, validToken)

class ValidateEmailView(GenericAPIView):
    # This view validate the user email
    # It takes as input a token, then it verify if it 
    # exists in the table of emailValidation, if it does
    # the reponse is 200, if it doesn't exists the response
    # is bad request
    def get(self, request, *args, **kwargs):
        if 'token' in request.query_params:
            token = request.query_params['token']
        else:
            return Response("No token provided", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            valid = EmailValidationToken.objects.get(token=token)
        except DoesNotExist:
            msg = {"detail": _("Your token is not valid.")} 
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            
        #TODO import django.timezone ... timezone.now
        
        #tmz = pytz.timezone(settings.TIME_ZONE)
        #expiration = (tmz.localize(datetime.datetime.now()) - valid.created_at)
        expiration = timezone.now() - valid.created_at
        
        # If the validation email was sent above 15 mins ago, then it expired
        if expiration.total_seconds()/60 > 15:
            valid.delete()
            msg = {"detail": _("Expired validation email! Go signup again.")} 
            return Response(msg, status=status.HTTP_200_OK)
        
        # remove the token and validate user account email_is_valid=true
        user = valid.user
        valid.delete()
        user.email_is_valid=True
        user.save()
        msg = {"detail": _("Your Email is now validated.")}
        return Response(msg, status=status.HTTP_200_OK)
    
# TODO :
"""
    DONE-Sign Up with email comfirmation
    -Login
    DONE-Update user information:
    -Update email
"""

class ResetPasswordView(GenericAPIView):
    #authentication_classes = (TokenAuthentication ) // No need
    # url/?email=email@mail.com
    serializer_class = PasswordResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        msg = {"detail": _("An email to reset your password was sent. Go check your emails.")}
        return Response(msg, status= status.HTTP_200_OK)

class ConfirmPasswordView(GenericAPIView):
    # This view reset the user password
    # It takes as input a token, then it verify if it 
    # exists in the table of PasswordResetToken, if it does
    # the reponse is 200, if it doesn't exists the response
    # is bad request
    
    serializer_class = ConfirmPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        msg = "Your password has been successfully updated."
        return Response(msg, status=status.HTTP_200_OK)
        
class LogoutView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    
    def get(self, request, *args, **kargs):
        usr = self.request.user
        #print (usr)
        msg = {"detail": _("Successfully logged out.")}
        
        try:
            token = Token.objects.get(user=usr)
        except DoesNotExist:
            pass
        
        token.delete()
        return Response(msg, status = status.HTTP_200_OK)

class LoginView(views.APIView):
    
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        #print (request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        try:
            token = Token.objects().get(user=user)
        except DoesNotExist:
            token = Token(user=user)
            token.save()
            
        return Response({'token': token.key})


#obtain_auth_token = ObtainAuthToken.as_view()
