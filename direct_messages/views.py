from rest_framework import generics, permissions
from sharesphere_drf_api.permissions import IsOwnerOrReadOnly
from .models import Message
from .serializers import MessageSerializer


class ListMessages(generics.ListCreateAPIView):
    """
    ListCreate view to view all messages and create new messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TargetMessage(generics.RetrieveDestroyAPIView):
    """
    RetrieveDestroy view to retrieve, or delete a message.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]