from rest_framework import serializers
from .models import User, Route, RouteMember, Point


# For now it only have non relationship fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('date', 'combustion', 'fuel_price', 'route_length')


class RouteMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteMember
        fields = 'route_price'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = 'address'