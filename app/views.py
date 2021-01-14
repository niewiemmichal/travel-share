from rest_framework import viewsets
from .models import User, RouteParticipant
from .serializers import UserSerializer, RouteParticipantSerializer


# list(), retrieve(), create(), update(), destroy()
class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RouteParticipantViewset(viewsets.ModelViewSet):
    queryset = RouteParticipant.objects.all()
    serializer_class = RouteParticipantSerializer
