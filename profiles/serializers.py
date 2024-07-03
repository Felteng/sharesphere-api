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


    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'created_at', 'image', 'bio', 'receieve_messages', 'is_owner']
        read_only_fields = ['id', 'created_at']