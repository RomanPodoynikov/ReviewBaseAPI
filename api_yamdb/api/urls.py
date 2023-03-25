from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet, 
                       ReviewViewSet, TitleViewSet, CreateTokenView, 
                       CreateUserView, GenreViewSet, UsersViewSet)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')

v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<reviews_id>[1-9]\d*)/comments',
    CommentViewSet,
    basename='comments'
)

v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls), name='api-root'),

    path('v1/auth/signup/', CreateUserView.as_view(), name='signup'),
    path('v1/auth/token/', CreateTokenView.as_view(), name='token'),
]