from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


class AuthorOrReadOnly(BasePermission):
    """Разрешение на уровне создатель"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
        )
