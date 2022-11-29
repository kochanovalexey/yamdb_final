from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Разрешение для админа или суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для админа или только для чтения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or IsAdminOrSuperUser().has_permission(request, view)
        )


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для автора, модератора, админа или только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        )
