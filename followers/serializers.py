from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


# Soruce:
# https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/followers/serializers.py
class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model

    Handles the representation and validation of Follower instances.
    The owner field represents the owner's username and followed_name
    represents the name of the user followed by the owner.

    The create method modifies the creation of a follow instance and attempts
    to create a follow with the validated data and handles IntegrityError in
    case of a duplicate instance by raising a validation error with a
    descriptive message.
    It further ensures that a user cannot be followed twice by the same user.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = ['id', 'owner', 'created_at', 'followed', 'followed_name']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})