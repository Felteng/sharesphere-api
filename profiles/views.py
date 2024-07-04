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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]