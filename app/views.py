from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Route
from .serializers import RouteReaderSerializer, RouteWriterSerializer, UserSerializer, UserDetailSerializer, \
    UserWriterSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            users = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            serializer = UserWriterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=request.data["email"])
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('User already exist', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserWriterSerializer(user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='email')
    def get_user_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)


class FriendsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        all_friends = user.friends.values_list('email', flat=True)
        users = User.objects.filter(email__in=all_friends)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        data = self.request.data
        new_friends = get_object_or_404(User.objects.all(), email=data["email"])
        user.friends.add(new_friends)
        serializer = UserSerializer(new_friends)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        data = self.request.data
        friend_to_delete = get_object_or_404(User.objects.all(), email=data["email"])
        user.friends.remove(friend_to_delete)
        return Response(status=status.HTTP_200_OK)


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
