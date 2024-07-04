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
        Check if the user making the request is the owner of the post.
        """
        return self.context.get('request').user == obj.owner


    # https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/posts/serializers.py#L15-L26
    def validate_image(self, value):
        """
        Validates image dimensions and file size to limit bandwidth usage and
        ensure that images fit the within the confinements of the frontend.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width is larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096px!'
            )
        return value


    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'created_at', 'updated_at', 'image', 'content', 'is_owner']
        read_only_fields = ['id', 'created_at', 'updated_at']