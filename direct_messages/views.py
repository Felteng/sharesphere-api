from django.db.models import Q
from rest_framework import generics, permissions
from sharesphere_drf_api.permissions import IsOwnerOrReceiver
from .models import Message
from .serializers import MessageSerializer


class ListMessages(generics.ListCreateAPIView):
    """
    ListCreate view to view all messages and create new messages.

    Only logged in users can intereact with and create direct messages.

    Use get_queryset method as opposed to variable to allow usage
    of the Q model, which treats filters as objects, allowing filtering
    with logical operators.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Queryset that ensures only the owner or receiver of a message
        can read it.
        """
        return Message.objects.filter(Q(owner=self.request.user) | Q(receiver=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TargetMessage(generics.RetrieveDestroyAPIView):
    """
    RetrieveDestroy view to retrieve, or delete a message.
    Retrieval is only allowed by the owner or the receiever and deletion
    is only allowed by the owner.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReceiver]