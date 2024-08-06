from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
         
        if request.user and request.user.is_staff:
            return True
        
        if request.user == obj.author:
            return True

        return False


class CommentsCustomPermissions(IsAuthorOrAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and request.user == obj.post.author:
            return True

        return super().has_object_permission(request, view, obj)
    

class ReactionsCustomPermissions(permissions.BasePermission):    
    def has_permission(self, request, view):
        if not request.user:
            return False
    
        if request.method == 'GET' and not request.user.is_staff:
            return False

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):         
        if request.user == obj.author:
            return True
        
        return False
