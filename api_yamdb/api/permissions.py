from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrPrivilegeduserOrReadOnly(BasePermission):
    """Просмотр контента - для всех, действия - для автора/персонала."""
    def has_permission(self, request, view):
        """
        Проверка прав п-ля на возможность действий на сайте.
        Для любого пользователя доступны только безопасные методы.
        """
        return request.user in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверка прав п-ля на возможность действий с объектом."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or request.user == obj.author
        )


class Admin_Only(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_staff


class TitlePermission(BasePermission):
    """
    Права доступа для админа и суперюзера на редактирование, удаление и
    добавление произведений, жанров и категорий.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
