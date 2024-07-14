from django.db import models
from django.contrib.auth.models import User
from direct_messages.models import Message


class Reply(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reply_sender'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reply_receiver'
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} replied to message: {self.message.id}'
