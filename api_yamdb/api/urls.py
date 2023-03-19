from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<reviews_id>[1-9]\d*])/comments/',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls), name='api-root'),
]