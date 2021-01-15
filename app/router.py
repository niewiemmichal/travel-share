from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, UserDetailViewset, Friends

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'user', UserDetailViewset, basename='users')
router.register(r'friends', Friends, basename='friends')
