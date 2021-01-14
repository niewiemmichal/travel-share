from rest_framework import serializers
from .models import User, Route, RouteParticipant, Landmark


# For now it only have non relationship fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('name', 'surname', 'email', 'password')


class RouteParticipantSerializer(serializers.ModelSerializer):
    participant = UserSerializer(many=False)

    class Meta:
        model = RouteParticipant
        fields = ('participant', 'price')


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = ('address',)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class RouteWriterSerializer(serializers.ModelSerializer):
    landmarks = LandmarkSerializer(many=True)
    participants = RouteParticipantSerializer(many=True)

    class Meta:
        model = Route
        fields = ('id', 'date', 'length', 'fuel_price', 'fuel_consumption', 'landmarks', 'participants')

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        landmarks_data = validated_data.pop('landmarks')
        route = Route.objects.create(**validated_data)
        for landmark_data in landmarks_data:
            Landmark.objects.create(route=route, **landmark_data)
        for participant_data in participants_data:
            user = User.objects.get(email=participant_data.get('participant').get('email'))
            RouteParticipant.objects.create(
                route=route,
                participant=user,
                price=participant_data.get('price'))
        return route


class RouteReaderSerializer(serializers.ModelSerializer):
    landmarks = LandmarkSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ('id', 'date', 'length', 'fuel_price', 'fuel_consumption', 'landmarks', 'participants')

    def get_participants(self, route_instance):
        query_data = RouteParticipant.objects.filter(route=route_instance)
        return [RouteParticipantSerializer(participant).data for participant in query_data]
