from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from . import models
from . import serializers


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        users = models.User.objects.all()
        return users

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            users = models.User.objects.get(email=request.data["email"])
        except models.User.DoesNotExist:
            serializer = serializers.UserWriterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('User already exist', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UserWriterSerializer(user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='email')
    def get_user_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class FriendsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        all_friends = user.friends.values_list('email', flat=True)
        users = models.User.objects.filter(email__in=all_friends)
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        data = self.request.data
        new_friends = get_object_or_404(models.User.objects.all(), email=data["email"])
        user.friends.add(new_friends)
        serializer = serializers.UserSerializer(new_friends)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        data = self.request.data
        friend_to_delete = get_object_or_404(models.User.objects.all(), email=data["email"])
        user.friends.remove(friend_to_delete)
        return Response(status=status.HTTP_200_OK)


