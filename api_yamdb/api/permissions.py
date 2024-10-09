from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Кастомный пермишен Админа."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsReviewOwnerOrReadOnly(BasePermission):
    """Кастомный пермишен отзыва."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or (request.user.is_admin or request.user.is_moderator))


class IsAdmin(BasePermission):
    """Кастомный пермишен Админа."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsSuperOrIsAdminOrIsModeratorOrIsAuthor(BasePermission):
    """Кастомный пермишен, аноним исключен."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)
        )
