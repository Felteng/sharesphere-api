from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model related to 'owner' (User model).

    Posts are ordered by when they were created with the newest
    ones visible at the top.

    Returns a str representation with the owner and title of each post
    to make it easier to identify a post.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='DEFAULTS/post_default'
        )
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner.username}: {self.title}'
