from django.shortcuts import render
from .models import Profile
from rest_framework import generics
from .serializers import ProfileSerializer


class ListProfiles(generics.ListAPIView):
    """
    ListAPIView to view all profiles. No need for a create view as profiles
    are created upon signup.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer