from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
         
        if request.user and request.user.is_staff:
            return True
        
        return False


class IsAuthorOrAdminOrReadOnly(IsAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True

        return super().has_object_permission(request, view, obj)


class CommentsCustomPermissions(IsAuthorOrAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and request.user == obj.post.author:
            return True

        return super().has_object_permission(request, view, obj)
