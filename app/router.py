from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, UserDetailViewset

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'user', UserDetailViewset, basename='user')
