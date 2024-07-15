from django.db.models import Q
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from sharesphere_drf_api.permissions import IsOwnerOrReceiver
from .models import Reply
from .serializers import ReplySerializer


class ListReplies(generics.ListCreateAPIView):
    """
    ListCreate view to view all messages and create new replies.

    Only logged in users can intereact with and create direct replies.

    Use get_queryset method as opposed to variable to allow usage
    of the Q model, which treats filters as objects, allowing filtering
    with logical operators.
    """
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Queryset that ensures only the owner or receiver of a reply
        can read it.
        """
        return Reply.objects.filter(
            Q(owner=self.request.user) | Q(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'message',
    ]


class TargetReply(generics.RetrieveDestroyAPIView):
    """
    RetrieveDestroy view to retrieve, or delete a reply.
    Retrieval is only allowed by the owner or the receiever and deletion
    is only allowed by the owner.
    """
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsOwnerOrReceiver]
