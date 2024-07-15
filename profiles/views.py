from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer
from .models import Profile


# https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/profiles/views.py
class ListProfiles(generics.ListAPIView):
    """
    List view to view all profiles. No need for a create view as profiles
    are created upon signup.

    Adds followers_count field to each post object using annotate().
    The Count is based on each profile's related `follower` object.
    Distinct=True ensures that each follower is only counted once in the case
    that the model's handling of duplicates was to fail.
    Also adds a following_count field similar to the likes_count field,
    as well as a post_count field related to the `post` object.

    Profiles can be filtered through searching the post owner's name or title.
    Post can also be filtered by posts made by a single owner,
    posts liked by a user, or posts from users that a user follows.
    """
    queryset = Profile.objects.annotate(
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
        post_count=Count('owner__post', distinct=True)
    )
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = [
        'owner__username',
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]
    ordering_fields = [
        'post_count'
    ]


class TargetProfile(generics.RetrieveUpdateAPIView):
    """
    RetrieveUpdate view to allow editing the details on a profile given
    that the request comes from the owner of the profile; IsOwnerOrReadOnly.
    """
    queryset = Profile.objects.annotate(
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
        post_count=Count('owner__post', distinct=True)
    )
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
