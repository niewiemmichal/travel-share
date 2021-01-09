# basic_api/models.py
from django.db import models


# DataFlair
class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    friends = models.ManyToManyField("self", verbose_name="list of friends", blank=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    date = models.DateField()
    fuel_consumption = models.FloatField()
    fuel_price = models.FloatField()
    route_length = models.FloatField()
    route_participants = models.ManyToManyField(User, through='RouteMember', through_fields=('route', 'participant'),
                                                blank=True)


class RouteMember(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    route_price = models.FloatField()


class Landmark(models.Model):
    address = models.CharField(max_length=100)
    getting_on_friends = models.ManyToManyField(User, verbose_name="list of friends getting on this point",
                                                related_name='+', blank=True)
    getting_off_friends = models.ManyToManyField(User, verbose_name="list of friends getting off this point",
                                                 related_name='+', blank=True)

    def __str__(self):
        return self.address
