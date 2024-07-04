from .models import Like
from rest_framework import generics, permissions
from .serializers import LikeSerializer
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly



class ListLikes(generics.ListCreateAPIView):
    """
    ListCreateAPIView to view all likes as well as create a like given
    user is authenticated.

    Override perform_create to ensure the owner field gets a value, the value
    will be that of the user performing the request.
    """
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class TargetLike(generics.RetrieveDestroyAPIView):
    """
    RetrieveDestroy view to allow deleting (unliking) any post given
    that the request comes from the owner of the like; IsOwnerOrReadOnly.
    """
    queryset = Like.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
