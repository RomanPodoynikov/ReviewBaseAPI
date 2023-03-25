from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrModeratorOrReadOnly(BasePermission):
    """Просмотр контента - для всех, действия - для автора/персонала."""
    def has_permission(self, request, view):
        """Проверка прав п-ля на возможность действий на сайте.
        Для любого пользователя доступны только безопасные методы .
        """
        return (request.user in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Проверка прав п-ля на возможность действий с объектом."""
        return (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class Admin_Only(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )
