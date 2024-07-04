from rest_framework import serializers
from .models import Like
from django.db import IntegrityError


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.

    This serializer handles the representation and validation of Like instances.
    The owner fields represents the owner's username.

    The create function modifies the creation of a like instance and attempts
    to create a like with the validated data and handles IntegrityError in
    case of a duplicate instance by raising a validation error with a
    descriptive message.
    It also ensures that the owner of a post can't like their own post.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'owner', 'post', 'created_at']
        read_only_fields = ['id', 'created_at']

    # Duplicate validation from:
    # https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/likes/serializers.py#L17-L23
    def create(self, validated_data):
        request = self.context.get('request')
        post = validated_data.get('post')

        if post.owner == request.user:
            raise serializers.ValidationError({
                'detail': 'You cannot like your own post.'
            })

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate like'
            })
