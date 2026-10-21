from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')

comments_router_v1 = DefaultRouter()
comments_router_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('v1/', include(router_v1.urls)),
    re_path(
        r'^v1/posts/(?P<post_id>\d+)/',
        include(comments_router_v1.urls)
    ),
]
