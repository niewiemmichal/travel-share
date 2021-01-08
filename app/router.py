from rest_framework import routers
from .views import UsersViewset

router = routers.DefaultRouter()
router.register('user', UsersViewset)