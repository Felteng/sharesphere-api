from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

# https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/drf_api/serializers.py
class CurrentUserSerializer(UserDetailsSerializer):
    """
    Extends the dj_rest_auth UserDetailsSerializer with 2 additional fields;
    profile_id and profile_image. This ensures that the profile id and image
    are both exposed in the api when fetching just the user model and not
    the whole profile model.
    """
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )