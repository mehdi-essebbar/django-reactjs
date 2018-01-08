from django.conf.urls import url

from .views import *

urlpatterns = [
    #Does not require quthentication
    url(r'^login/$', LoginView.as_view(), name=r"login"), # post: username, password
    url(r'^registration/$', SignUpView.as_view(), name=r"signup"), # post: username, email, password1, password2
    url(r'^registration/verify-email/$', ValidateEmailView.as_view(), name=r"verify_email"), # get: with params ?token={token}
    url(r'^password/reset/$', ResetPasswordView.as_view(), name=r"pwd_reset"), # post: email
    url(r'^password/reset/confirm/$', ConfirmPasswordView.as_view(), name=r"pwd_confirm"), # post: new_password1, new_password2, token
    
    # require authentication
    url(r'^logout/$', LogoutView.as_view(), name=r"logout"), # get + authentication header
    url(r'^password/change/$', PasswordChangeView.as_view(), name=r"pwd_change"), # post: old_password, new_password1, new_password2
    url(r'^user/$', UserView.as_view(), name=r"user_profile"), # post+get
]
