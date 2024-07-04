from .models import Post
from rest_framework import generics, permissions, filters
from .serializers import PostSerializer
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class ListPosts(generics.ListCreateAPIView):
    """
    ListCreateAPIView to view all posts as well as create a post given
    user is authenticated.

    Override perform_create to ensure the owner field gets a value, the value
    will be that of the user performing the request.

    Posts can be filtered through searching the post owner's name or title as
    well as filtered by posts made by a single owner.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    filterset_fields = [
        'owner__profile'
    ]