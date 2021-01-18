from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User, Route
from .serializers import RouteReaderSerializer, RouteWriterSerializer


class RoutesViewSet(viewsets.ViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteReaderSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
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
