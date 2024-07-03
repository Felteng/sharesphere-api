from rest_framework import permissions


# Source for the following object permission implementation:
# https://www.django-rest-framework.org/api-guide/permissions/#isauthenticatedorreadonly:~:text=class%20IsOwnerOrReadOnly(,request.user
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    'if request.method in permissions.SAFE_METHODS' ensures that any request
    has read permission.

    Write permissions will only be allowed to the obj.owner of the profile.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
