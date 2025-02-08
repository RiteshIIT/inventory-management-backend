from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework.authtoken.views import obtain_auth_token

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('',  include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth')   
]