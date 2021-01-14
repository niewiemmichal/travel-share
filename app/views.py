from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User, RouteParticipant, Route
from .serializers import UserSerializer, RouteParticipantSerializer, RouteReaderSerializer, RouteWriterSerializer


# list(), retrieve(), create(), update(), destroy()
class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RouteParticipantViewset(viewsets.ModelViewSet):
    queryset = RouteParticipant.objects.all()
    serializer_class = RouteParticipantSerializer


class RoutesViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteReaderSerializer

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        routes = Route.objects.filter(participants=user)
        serializer = RouteReaderSerializer(routes, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = RouteWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            route = write_serializer.save()
            read_serializer = RouteReaderSerializer(route)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)