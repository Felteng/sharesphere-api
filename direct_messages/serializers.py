from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Adds receiver_name field as the model's receiver field cannot be read only
    since the owner (sender) has to be able to choose a receiver.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.profile.id')
    owner_image = serializers.ReadOnlyField(
        source='receiver.profile.image.url'
        )
    receiver_image = serializers.ReadOnlyField(
        source='owner.profile.image.url'
        )
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    replies_count = serializers.ReadOnlyField()
    created_at = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_receiver = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the message.
        """
        return self.context.get('request').user == obj.owner

    def get_is_receiver(self, obj):
        """
        Check if the user making the request is the receiver of the message.
        """
        return self.context.get('request').user == obj.receiver

    def get_created_at(self, obj):
        """
        Display creation time in comparative format.
        """
        return naturaltime(obj.created_at)

    def create(self, validated_data):
        """
        Performs a check when a post request is made to ensure that
        a user doesn't send a message to themselves.
        """
        owner = self.context.get('request').user
        if validated_data['receiver'] == owner:
            raise serializers.ValidationError(
                "You can't send a message to yourself"
            )
        return super().create(validated_data)

    class Meta:
        model = Message
        fields = [
            'id', 'owner', 'receiver_name', 'receiver', 'topic', 'created_at',
            'content', 'is_owner', 'is_receiver', 'replies_count',
            'owner_image', 'owner_id', 'receiver_image'
        ]
        read_only_fields = ['id']
