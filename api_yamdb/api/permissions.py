from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (obj.author == request.user or request.method in SAFE_METHODS)
        )


class IsAdmin(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""

    def has_permission(self, request, view):
        return request.user.is_moderator or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator or request.user.is_superuser


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_moderator
                 or request.user.is_superuser
                 or obj.author == request.user)
        )
