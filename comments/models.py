from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Soruce:
# https://github.com/Felteng/drf-api/blob/main/comments/models.py
class Comment(models.Model):
    """
    Like model, related to 'owner' and 'post'.

    Comments are ordered by when they were created with the newest ones
    visible at the top.
    Returns a str representation of each comment to make it easier to
    identify its content.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
