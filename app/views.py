from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers


# list(), retrieve(), create(), update(), destroy()
class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        users = models.User.objects.all()
        return users

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.UserDetailSerializer
        return serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = models.User.objects.get(pk=kwargs['pk'])
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)


class UserDetailViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('friends__name')
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


@api_view(['GET', 'POST'])
def friends(request, pk_user):
    try:
        user = models.User.objects.get(pk=pk_user)
    except models.User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        friends = user.friends.values_list('email', flat=True)
        users = models.User.objects.filter(email__in=friends)
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        friend = models.User.objects.get(email=data["email"])
        user.friends.add(friend)
        serializer = serializers.UserSerializer(friend)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['DELETE'])
def friend_delete(request, pk_user, pk_friend):
    try:
        user = models.User.objects.get(pk=pk_user)
    except models.User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'DELETE':
        user_to_delete = models.User.objects.get(pk=pk_friend)
        user.friends.remove(user_to_delete)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_by_email(request, email_user):
    try:
        user = models.User.objects.get(email=email_user)
    except models.User.DoesNotExist:
        return HttpResponse(status=404)

    serializer = serializers.UserSerializer(user)
    return Response(serializer.data)
