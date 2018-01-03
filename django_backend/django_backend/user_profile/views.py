from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import UserProfile

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
