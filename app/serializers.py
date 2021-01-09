from rest_framework import serializers
from .models import User, Route, RouteMember, Landmark


# For now it only have non relationship fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
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
        model = Landmark
        fields = 'address'