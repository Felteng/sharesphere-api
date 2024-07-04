from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Sets the owner field to display the username of the owner.
    Adds is_owner field to display a boolean of whether the user is the owner
    of a profile in a request.
    Adds following_id field to display the id of the follower instance if the
    user of the requet follows a particular profile.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the profile
        """
        return self.context.get('request').user == obj.owner

    def validate_image(self, value):
        """
        Validates profile image file size to limit bandwidth usage.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        return value

    # https://github.com/Felteng/drf-api/blob/93b2ef26776968cb1386f1f025e7c98645b21ad4/profiles/serializers.py#L22-L29
    def get_following_id(self, obj):
        """
        If the user making the request is following a particular profile
        return the the id of that follower instance. If the user is not
        following the user return None making following_id = null.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'created_at', 'image', 'bio', 'receieve_messages', 'following_id', 'is_owner']
        read_only_fields = ['id', 'created_at']