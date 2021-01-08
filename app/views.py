from rest_framework import viewsets
from . import models
from . import serializers


# list(), retrieve(), create(), update(), destroy()
class UsersViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

