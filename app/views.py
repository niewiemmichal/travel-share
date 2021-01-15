from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.decorators import api_view
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
        user = models.User.objects.get(pk=kwargs['pk'])
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            users = models.User.objects.get(email=request.data["email"])
        except models.User.DoesNotExist:
            data = request.data
            new_user = models.User.objects.create(name=data["name"], surname=data["surname"], email=data["email"],
                                              password=data["password"])
            new_user.save()
            serializer = serializers.UserWriterSerializer(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response('User already exist', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = serializers.UserWriterSerializer(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='email')
    def get_user_by_email(self, request):
        email = request.GET.get('email', '')
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class UserDetailViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        new_user = models.User.objects.create(name=data["name"], surname=data["surname"], email=data["email"],
                                              password=data["password"])
        new_user.save()
        for user in data["friends"]:
            user_obj = models.User.objects.get(email=user["email"])
            new_user.friends.add(user_obj)

        serializer = serializers.UserDetailSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Friends(viewsets.ViewSet):

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

        data = request.data
        new_friends = get_object_or_404(models.User.objects.all(), email=data["email"])
        user.friends.add(new_friends)
        serializer = serializers.UserSerializer(new_friends)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        data = request.data
        friend_to_delete = get_object_or_404(models.User.objects.all(), email=data["email"])
        user.friends.remove(friend_to_delete)
        return Response(status=status.HTTP_200_OK)


