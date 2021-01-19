from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, FriendsViewSet, RoutesViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'friends', FriendsViewSet, basename='friends')
router.register('routes', RoutesViewSet, basename='routes')
