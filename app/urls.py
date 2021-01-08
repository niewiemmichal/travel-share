from django.urls import path, include
from .router import router

urlpatterns = [
    path('get-users/', include(router.urls))
]