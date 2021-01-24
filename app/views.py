from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Route
from .permissions import UserAccessPermission
from .serializers import RouteReaderSerializer, RouteWriterSerializer, UserSerializer, UserDetailSerializer


class UsersViewSet(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='email')
    def retrieve_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [UserAccessPermission]
        elif self.action == 'retrieve_by_email':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


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
        try:
            new_friend = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if new_friend == user:
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)
        else:
            friends = user.friends.filter(email=data["email"])
            if friends:
                return Response("Already exists", status=status.HTTP_400_BAD_REQUEST)
            else:
                user.friends.add(new_friend)
                serializer = UserSerializer(new_friend)
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

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [UserAccessPermission]
        elif self.action == 'update':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class RoutesViewSet(viewsets.ViewSet):

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

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [UserAccessPermission]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
