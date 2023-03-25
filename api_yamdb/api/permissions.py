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
        return bool(request.method in SAFE_METHODS
                    or request.user and (
                        request.user.is_authenticated or request.user.is_staff
                    ))

    def has_object_permission(self, request, view, obj):
        """Проверка прав п-ля на возможность действий с объектом."""
        if obj.author != request.user or not (
            request.user or request.user.is_staff
        ):
            return request.method in SAFE_METHODS
        return True


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
