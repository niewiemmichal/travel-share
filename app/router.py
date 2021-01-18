from rest_framework import routers
from .views import RoutesViewSet

router = routers.DefaultRouter()
router.register('routes', RoutesViewSet)
