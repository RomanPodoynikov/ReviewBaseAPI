from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrPrivilegeduserOrReadOnly(BasePermission):
    """Просмотр контента - для всех, действия - для автора/персонала."""
    def has_permission(self, request, view):
        """
        Проверка прав п-ля на возможность действий на сайте.
        Для любого пользователя доступны только безопасные методы.
        """
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверка прав п-ля на возможность действий с объектом."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or request.user == obj.author
        )


class IsAuthenticatedAndAdminOrReadOnly(BasePermission):
    """
    Права доступа для админа и суперюзера на редактирование, удаление и
    добавление.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )
