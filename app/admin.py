from django.contrib import admin
from .models import User, Route, RouteParticipant, Landmark

admin.site.register(User)
admin.site.register(Route)
admin.site.register(RouteParticipant)
admin.site.register(Landmark)
