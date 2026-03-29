from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBrokerOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return getattr(user, "role", None) == "broker"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        return getattr(user, "role", None) == "broker" and obj.broker == user