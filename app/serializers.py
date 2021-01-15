from rest_framework import serializers
from .models import User, Route, RouteParticipant, Landmark


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'email', 'friends')


class UserWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('date', 'combustion', 'fuel_price', 'route_length')


class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('date', 'combustion', 'fuel_price', 'route_length')


class RouteMemberSerializer(serializers.ModelSerializer):
    participant = UserSerializer(many=True, required=False, read_only=True)
    route = RouteSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = RouteParticipant
        fields = ('route_price', 'participant', 'route')


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = 'address'
