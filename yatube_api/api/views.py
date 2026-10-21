from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post

from .mixins import AuthorOnlyMixin
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(AuthorOnlyMixin, viewsets.ModelViewSet):
    """CRUD для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(AuthorOnlyMixin, viewsets.ModelViewSet):
    """CRUD для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_post(self):
        """Возвращает пост по id или 404."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает комментарии поста."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создаёт комментарий с автором и постом."""
        serializer.save(
            author=self.request.user,
            post=self.get_post(),
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
