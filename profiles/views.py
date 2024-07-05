from rest_framework import generics
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer
from .models import Profile


class ListProfiles(generics.ListAPIView):
    """
    List view to view all profiles. No need for a create view as profiles
    are created upon signup.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class TargetProfile(generics.RetrieveUpdateAPIView):
    """
    RetrieveUpdate view to allow editing the details on a profile given
    that the request comes from the owner of the profile; IsOwnerOrReadOnly.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]