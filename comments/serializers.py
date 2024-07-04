from rest_framework import serializers
from .models import Comment
from django.contrib.humanize.templatetags.humanize import naturaltime


# Source:
# https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/comments/serializers.py
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Adds 3 additional fields:
    A boolean of whether the user making the request if the comment owner.
    The profile image of the comment owner.
    The profile id of the comment owner.

    Converts the created and updated at fields to use a natural time format.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    is_owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the profile
        """
        return self.context.get('request').user == obj.owner


    def get_created_at(self, obj):
        """
        Naturaltime renders datetime in a comparative format
        eg. created 1 day, 7 hours ago
        """
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'profile_id', 'profile_image', 'post', 'content', 'created_at', 'updated_at', 'is_owner']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TagetCommentSerializer(CommentSerializer):
    """
    Extends the CommentSerializer to make 'post' a read only field.
    Making post a read only field makes it so it does not have to be set
    whenever an update is performed, it also ensures a comment can't be
    moved to different post.
    """
    post = serializers.ReadOnlyField(source='post.id')
