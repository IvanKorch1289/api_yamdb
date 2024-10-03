from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser is True)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser is True)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.is_superuser is True

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator' or request.user.is_superuser is True
