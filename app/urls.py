from django.urls import path, include
from .router import router

urlpatterns = [
    path('users/', include(router.urls))
]