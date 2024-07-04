from rest_framework import generics, permissions
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class ListFollowers(generics.ListCreateAPIView):
    """
    ListCreateAPIView to view all follower instances as well as create a
    follow given user is authenticated.
    
    Override perform_create to ensure the owner field gets a value, the value
    will be that of the user performing the request.
    """
    queryset = Follower.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class TargetFollower(generics.RetrieveDestroyAPIView):
    """
    RetrieveDestroy view to allow deleting (unfollowing) any user given
    that the request comes from the owner of the follow; IsOwnerOrReadOnly.
    """
    queryset = Follower.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
