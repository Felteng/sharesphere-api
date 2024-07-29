from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message


class TestMessagesViews(TestCase):

    def setUp(self):
        """User and Message creation setup"""
        self.user1 = User.objects.create_user(
            username="myUsername1",
            password="myPassword1",
        )
        self.user2 = User.objects.create_user(
            username="myUsername2",
            password="myPassword2",
        )
        self.user3 = User.objects.create_user(
            username="myUsername3",
            password="myPassword3",
        )
        self.message = Message.objects.create(
            owner=self.user1,
            receiver=self.user2,
            topic="test topic",
            content="test content"
            )

    def test_message_creation(self):
        """Test that message creation was successful"""
        self.assertEqual(
            Message.objects.count(), 1,
            "There are more or less than 1 messages created"
        )
        self.assertEqual(
            self.message.owner.username, "myUsername1",
            msg="myUsername1 is not the owner"
        )
        self.assertEqual(
            self.message.receiver.username, "myUsername2",
            msg="myUsername2 is not the receiver"
        )

    def test_retrieve_message_in_list_as_owner(self):
        """Test that the owner can see the message in the /messages list"""
        self.client.login(username="myUsername1", password="myPassword1")
        response = self.client.get(
            reverse('list_messages')
        )
        self.assertEqual(
            response.status_code, 200,
            msg='User could not retrieve message list'
        )

        for message in response.data['results']:
            """Loop through list of messages to find created message"""
            if message['id'] == self.message.pk:
                self.assertEqual(
                    message['topic'], self.message.topic,
                    msg='Message topic in list does not match'
                )
                self.assertEqual(
                    message["is_owner"], True,
                    msg='User 1 is not owner of the message in the list'
                )
                self.assertEqual(
                    message['is_receiver'], False,
                    msg='User 1 is the receiver of the message in the list'
                )
                break

    def test_retrieve_message_in_list_as_receiver(self):
        """Test that the receiver can see the message in the /messages list"""
        self.client.login(username="myUsername2", password="myPassword2")
        response = self.client.get(
            reverse('list_messages')
        )
        self.assertEqual(
            response.status_code, 200,
            msg='User could not retrieve message list'
        )

        for message in response.data['results']:
            """Loop through list of messages to find created message"""
            if message['id'] == self.message.pk:
                self.assertEqual(
                    message['topic'], self.message.topic,
                    msg='Message topic in list does not match'
                )
                self.assertEqual(
                    message["is_owner"], False,
                    msg='User 2 is the owner of the message in the list'
                )
                self.assertEqual(
                    message['is_receiver'], True,
                    msg='User 2 is not the receiver of the message in the list'
                )
                break

    def test_retrieve_message_in_list_as_other_user(self):
        """Test that another user can't see message in the /messages list"""
        self.client.login(username="myUsername3", password="myPassword3")
        response = self.client.get(
            reverse('list_messages')
        )
        self.assertEqual(
            response.status_code, 200,
            msg='User could not retrieve message list'
        )

        for message in response.data['results']:
            """
            Loop through list of messages to find created message.
            If message is found forces test to fail.
            """
            if message['id'] == self.message.pk:
                self.fail('Message is visible for user 3 in messages list')

    def test_retrieve_message_by_owner(self):
        """Test that the owner can retrieve the message"""
        self.client.login(username="myUsername1", password="myPassword1")
        response = self.client.get(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 200,
            msg='User 1 does not have access to message'
        )
        self.assertEqual(
            response.data['topic'], self.message.topic,
            msg='Message topic does not match, is the wrong message rendered?'
        )
        self.assertEqual(
            response.data['is_owner'], True,
            msg='User 1 is not the message owner'
        )
        self.assertEqual(
            response.data['is_receiver'], False,
            msg='User 1 is the message receiver'
        )

    def test_retrieve_message_by_receiver(self):
        """Test that the receiver can retrieve the message"""
        self.client.login(username="myUsername2", password="myPassword2")
        response = self.client.get(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 200,
            msg='User 2 does not have access to message'
        )
        self.assertEqual(
            response.data['topic'], self.message.topic,
            msg='Message topic does not match, is the wrong message rendered?'
        )
        self.assertEqual(
            response.data['is_owner'], False,
            msg='User 2 is the message owner'
        )
        self.assertEqual(
            response.data['is_receiver'], True,
            msg='User 2 is not the message receiver'
        )

    def test_retrieve_message_by_other_user(self):
        """Test that another user cannot retrieve the message"""
        self.client.login(username="myUsername3", password="myPassword3")
        response = self.client.get(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 403,
            msg='User 3 is not forbidden to access message'
        )

    def test_delete_message_by_owner(self):
        """Test that the owner can delete the message"""
        self.client.login(username="myUsername1", password="myPassword1")
        response = self.client.delete(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 204,
            msg='User 1 cannot delete message'
        )
        self.assertEqual(
            Message.objects.count(), 0,
            msg='Message was not successfully deleted'
        )

    def test_delete_message_by_receiver(self):
        """Test that the receiver cannot delete the message"""
        self.client.login(username="myUsername2", password="myPassword2")
        response = self.client.delete(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 403,
            msg='User 2 is not forbidden to delete message'
        )

    def test_delete_message_by_other_user(self):
        """Test that another user cannot delete the message"""
        self.client.login(username="myUsername3", password="myPassword3")
        response = self.client.delete(
            reverse('target_message', args=[self.message.pk])
        )
        self.assertEqual(
            response.status_code, 403,
            msg='User 3 is not forbidden to access/delete message'
        )
