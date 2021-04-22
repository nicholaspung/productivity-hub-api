from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, User):
            return obj == request.user

        if not hasattr(obj, 'user'):
            if hasattr(obj, 'profile'):
                return obj.profile.user == request.user

        return obj.user == request.user


IsAuthenticatedAndOwner = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]
