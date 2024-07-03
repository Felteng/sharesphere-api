from .models import Post
from rest_framework import generics, permissions, filters
from .serializers import PostSerializer
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly


class ListPosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = [
        'owner__username',
        'title',
    ]