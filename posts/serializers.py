from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the post
        """
        return self.context.get('request').user == obj.owner


    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'created_at', 'updated_at', 'image', 'content', 'is_owner']
        read_only_fields = ['id', 'created_at', 'updated_at']