from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, signup,
                    TitleViewSet, token, UserViewSet,
                    ReviewViewSet, CommentViewSet)

app_name = 'api'

v1_router = routers.SimpleRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'categories', CategoryViewSet, basename='categories')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token')
]

v1_urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
