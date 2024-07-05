from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Message
from replies.serializers import ReplySerializer


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Adds receiver_name field as the model's receiver field cannot be read only
    since the owner (sender) has to be able to choose a receiver.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    created_at = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_receiver = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

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

    def get_replies(self, obj):
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True, context=self.context).data

    def create(self, validated_data):
        """
        Performs a check when a post request is made to ensure that
        a user doesn't send a message to themselves.
        """
        owner = self.context.get('request').user
        if validated_data['receiver'] == owner:
            raise serializers.ValidationError("You can't send a message to yourself")
        return super().create(validated_data)
        

    class Meta:
        model = Message
        fields = ['id', 'owner', 'receiver_name', 'receiver', 'topic', 'created_at', 'content', 'is_owner', 'is_receiver', 'replies']
        read_only_fields = ['id']

