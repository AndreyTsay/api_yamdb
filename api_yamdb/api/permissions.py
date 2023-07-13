from rest_framework import permissions

from users.models import ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только аутентифицированному пользователю с ролью admin.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return request.method in permissions.SAFE_METHODS


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только суперпользователю Джанго, админу Джанго или
    аутентифицированному пользователю с ролью admin.
    """

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin)


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю Джанго, админу Джанго, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))
