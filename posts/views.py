from .models import Post
from rest_framework import generics, permissions
from .serializers import PostSerializer
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly


class ListPosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer