from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

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

    # https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/posts/serializers.py#L32-L39
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'title', 'created_at', 'updated_at', 'image',
            'content', 'likes_count', 'comments_count', 'is_owner',
            'profile_image', 'profile_id', 'like_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']