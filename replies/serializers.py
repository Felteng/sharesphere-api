from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Reply


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializer for the Reply model.

    Adds receiver_name field as the model's receiver field cannot be read only
    since the owner (sender) has to be able to choose a receiver.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')
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
        Sets the receiver of the reply to the user of the original message
        that did not make the post request.
        
        This ensures that the owner of the reply can always be fetched
        so that replies can be deleted by the appropriate user.
        """
        owner = self.context.get('request').user
        message = validated_data['message']
        validated_data['receiver'] = message.receiver if owner == message.owner else message.owner
        return super().create(validated_data)
        

    class Meta:
        model = Reply
        fields = ['id', 'owner', 'receiver', 'message', 'created_at', 'content', 'is_owner', 'is_receiver']
        read_only_fields = ['id']

