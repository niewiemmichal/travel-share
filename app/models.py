from django.db import models

from users.models import CustomUser as User


class Route(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    length = models.FloatField()
    fuel_price = models.FloatField()
    fuel_consumption = models.FloatField()
    participants = models.ManyToManyField(User, through='RouteParticipant', through_fields=('route', 'participant'),
                                          blank=True)


class RouteParticipant(models.Model):
    price = models.FloatField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, related_name='participants', on_delete=models.CASCADE)


class Landmark(models.Model):
    address = models.CharField(max_length=100)
    route = models.ForeignKey(Route, related_name='landmarks', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.address
