from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, TagetCommentSerializer


class ListComments(generics.ListCreateAPIView):
    """
    ListCreate view to view all comments as well as create a comment given
    user is authenticated.

    Override perform_create to ensure the owner field gets a value, the value
    will be that of the user performing the request.
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'post',
    ]


class TargetComment(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveDestroy view to allow deleting (unliking) any post given
    that the request comes from the owner of the like; IsOwnerOrReadOnly.
    """
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TagetCommentSerializer
