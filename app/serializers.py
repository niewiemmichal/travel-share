from rest_framework import serializers
from .models import User, Route, RouteParticipant, Landmark


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'friends')

        
class ParticipantReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        
class ParticipantWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {
            'email': {'validators': []},
        }

        
class RouteParticipantWriterSerializer(serializers.ModelSerializer):
    participant = ParticipantWriterSerializer(many=False)

    class Meta:
        model = RouteParticipant
        fields = ('participant', 'price')


class RouteParticipantReaderSerializer(serializers.ModelSerializer):
    participant = ParticipantReaderSerializer(many=False, read_only=True)
    
    class Meta:
        model = RouteParticipant
        fields = ('participant', 'price')
        

class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = ('address',)


class RouteWriterSerializer(serializers.ModelSerializer):
    landmarks = LandmarkSerializer(many=True)
    participants = RouteParticipantWriterSerializer(many=True)

    class Meta:
        model = Route
        fields = ('name', 'date', 'length', 'fuel_price', 'fuel_consumption', 'landmarks', 'participants')

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        users = []
        for participant_data in participants_data:
            try:
                users.append({
                    "user": User.objects.get(email=participant_data.get('participant').get('email')),
                    "price": participant_data.get('price')
                })
            except Exception as e:
                error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
                raise serializers.ValidationError(error)
        landmarks_data = validated_data.pop('landmarks')
        route = Route.objects.create(**validated_data)
        for landmark_data in landmarks_data:
            Landmark.objects.create(route=route, **landmark_data)
        for user in users:
            RouteParticipant.objects.create(
                route=route,
                participant=user.get("user"),
                price=user.get('price'))
        return route


class RouteReaderSerializer(serializers.ModelSerializer):
    landmarks = LandmarkSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ('name', 'date', 'length', 'fuel_price', 'fuel_consumption', 'landmarks', 'participants')

    def get_participants(self, route_instance):
        query_data = RouteParticipant.objects.filter(route=route_instance)
        return [RouteParticipantReaderSerializer(participant).data for participant in query_data]
