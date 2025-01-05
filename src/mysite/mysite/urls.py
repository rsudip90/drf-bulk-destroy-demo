from django.urls import path, include
from rest_framework.authtoken import views as drf_views

from .router import APIRouter

# url registrations
urlpatterns = [
    path("api/v1/", include(APIRouter.urls)),
    path("api/v1/api-token-auth/", drf_views.obtain_auth_token)
]
