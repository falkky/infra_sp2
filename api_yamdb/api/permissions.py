from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class AuthorOrModearatorOrAdminChangePermission(permissions.BasePermission):
    """Разрешаем доступ всем сейф методами или аутинтифицированным пользователям.
    Изменять объекты могут либо авторы, либо определенные роли.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user == obj.author or request.user.role in (
                MODERATOR, ADMIN,))


class AdminOnly(permissions.BasePermission):
    """Разрешаем доступ только пользователю с ролью admin или superuser."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == ADMIN or request.user.is_superuser


class AdminEdit(permissions.BasePermission):
    """Разрешаем чтение всем пользователям,
    создание и удаление с ролью admin или superuser.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == ADMIN or request.user.is_superuser
