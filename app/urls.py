from django.urls import path, include
from .router import router
from . import views

urlpatterns = [
    path('', include(router.urls)),
    path('friends/<pk_user>', views.friends, name="friends-list"),
    path('friends/<pk_user>/<pk_friend>', views.friend_delete, name="friends-list")
    #(?P<pk>[0-9]+)/$
]