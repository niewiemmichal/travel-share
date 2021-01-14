from rest_framework import routers
from .views import UsersViewset, RoutesViewset, RouteParticipantViewset

router = routers.DefaultRouter()
router.register('users', UsersViewset),
router.register('routes', RoutesViewset),
router.register('route_participants', RouteParticipantViewset),
