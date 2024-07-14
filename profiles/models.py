from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Credit to code institute for various solutions used in this model:
# https://github.com/Code-Institute-Solutions/drf-api/blob/ed54af9450e64d71bc4ecf16af0c35d00829a106/profiles/models.py
class Profile(models.Model):
    """
    User profile model extending the base User model with various new fields:
    name, creation date, profile image, bio, and message preferences.

    Profiles are ordered by when they were created with the newest
    ones visible at the top.

    Returns a str representation of each profile to make it easier to
    identify whose profile it is.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='images/', default='DEFAULTS/profile_default'
        )
    bio = models.CharField(max_length=300, blank=True)
    receive_messages = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} - Profile'


def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function that creates a profile when a user is created
    """
    if created:
        Profile.objects.create(owner=instance)


# Signal to trigger create_profile function whenever a user is created
post_save.connect(create_profile, sender=User)
