from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import CreateUserViewSet, CreateTokenViewSet, UsersViewSet

app_name = 'user'

v1_router = DefaultRouter()
v1_router.register('signup', CreateUserViewSet, basename='signup')
v1_router.register('token', CreateTokenViewSet, basename='token')
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('', include(v1_router.urls)),
]