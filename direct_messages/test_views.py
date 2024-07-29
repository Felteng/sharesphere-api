from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Message


class TestDetailViews(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="myUsername1",
            password="myPassword1",
        )
        self.user2 = User.objects.create_user(
        username="myUsername2",
        password="myPassword2",
        )
        self.message = Message(
            owner=self.user1,
            receiver=self.user2,
            topic="test topic",
            content="test content"
            )
        self.message.save()


    def test_message_creation(self):
        self.assertEqual(Message.objects.count(), 1, "There are more or less than 1 messages created")
        self.assertEqual(self.message.owner.username, "myUsername1", msg="myUsername1 is not the owner")
        self.assertEqual(self.message.receiver.username, "myUsername2", msg="myUsername2 is not the receiver")
