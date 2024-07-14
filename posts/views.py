from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class ListPosts(generics.ListCreateAPIView):
    """
    ListCreate view to view all posts as well as create a post given
    user is authenticated.

    Adds likes_count field to each post object using annotate().
    The Count is based on each post's related `Like` object.
    Distinct=True ensures that each like is only counted once in the case
    that the model's handling of duplicates was to fail.
    Also adds a comments_count field similar to the likes_count field.

    Override perform_create to ensure the owner field gets a value, the value
    will be that of the user performing the request.

    Posts can be filtered through searching the post owner's name or title.
    Post can also be filtered by posts made by a single owner,
    posts liked by a user, or posts from users that a user follows.
    """
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')
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
        'owner__profile',
        'likes__owner__profile',
        'owner__followed__owner__profile'
    ]


class TargetPost(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroy view to allow editing or deleting any post given
    that the request comes from the owner of the post; IsOwnerOrReadOnly.
    """
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
