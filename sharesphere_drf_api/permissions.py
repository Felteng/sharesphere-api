from rest_framework import permissions


# Source for the following object permission implementation:
# https://www.django-rest-framework.org/api-guide/permissions/#isauthenticatedorreadonly:~:text=class%20IsOwnerOrReadOnly(,request.user
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    'if request.method in permissions.SAFE_METHODS' ensures that any request
    has read permission.

    Write permissions will only be allowed to the obj.owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwnerOrReceiver(permissions.BasePermission):
    """
    Custom permission intended for messages and replies to only allow owners
    and receivers of a message to view it whilst only allowing the owners to
    edit it.

    Ensures that the receiver will always have read permission.
    Write and read permissions will only be allowed to the obj.owner.
    """
    def has_object_permission(self, request, view, obj):
        if (
            obj.receiver == request.user and
            request.method in permissions.SAFE_METHODS
        ):
            return True
        return obj.owner == request.user
