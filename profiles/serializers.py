from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the profile
        """
        return self.context.get('request').user == obj.owner

    # https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/posts/serializers.py#L15-L17
    def validate_image(self, value):
        """
        Validates profile image file size to limit bandwidth usage.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        return value


    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'created_at', 'image', 'bio', 'receieve_messages', 'is_owner']
        read_only_fields = ['id', 'created_at']