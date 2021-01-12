from django.urls import path, include
from .router import router
from . import views

urlpatterns = [
    path('', include(router.urls)),
    path('friends/<pk_user>', views.friends, name="friends-list"),
    path('friends/<pk_user>/<pk_friend>', views.friend_delete, name="friends-list"),
    path('users/email/<email_user>', views.user_by_email, name="user-by-email")
    #(?P<pk>[0-9]+)/$
]