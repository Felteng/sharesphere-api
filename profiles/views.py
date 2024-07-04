from .models import Profile
from rest_framework import generics
from .serializers import ProfileSerializer
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly


class ListProfiles(generics.ListAPIView):
    """
    ListAPIView to view all profiles. No need for a create view as profiles
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