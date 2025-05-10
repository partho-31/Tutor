from rest_framework import permissions


class IsAdminOrTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role == 'Teacher':
            return True
        return bool(request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return obj.teacher == request.user
    


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)



class OnlyForTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'Teacher':
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)


class StudentCanReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role == 'Teacher':
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)
 
    
class ReviewAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return obj.user == request.user