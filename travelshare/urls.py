from allauth.account.views import confirm_email
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='TravelShare API')


urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls'))
]
