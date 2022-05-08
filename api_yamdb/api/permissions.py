from django.contrib.auth import get_user_model
from rest_framework import permissions

from .utils import common_permission

User = get_user_model()


class GenreCategoryPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return common_permission(request, ['POST', 'DELETE', 'PATCH'])

    def has_object_permission(self, request, view, obj):
        return request.method == 'DELETE'


class TitlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return common_permission(request, ['POST', 'DELETE', 'PATCH'])

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method in ['DELETE', 'PATCH']
        )


class OwnerAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.role in (User.ADMIN, User.MODERATOR)
        )


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.admin
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
