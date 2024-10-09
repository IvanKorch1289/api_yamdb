from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAnonim(BasePermission):
    """Кастомный пермишен Анонима."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Кастомный пермишен Админа."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsSuperUserIsAdminIsModeratorIsAuthor(BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю, админу, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )
