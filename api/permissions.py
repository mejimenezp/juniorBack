from rest_framework import permissions
from .models import UsuarioRol, RolPermiso, UsuarioPermiso

class IsUserWithRole(permissions.BasePermission):
    def has_permission(self, request, view):
       
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            return True 

        user = request.user
        if not user.is_authenticated:
            return False

       
        return UsuarioRol.objects.filter(usuario=user, rol__nombre=required_role).exists()

class IsUserWithPermission(permissions.BasePermission):
    def has_permission(self, request, view):
    
        required_permission = getattr(view, 'required_permission', None)
        if required_permission is None:
            return True  

        user = request.user
        if not user.is_authenticated:
            return False

        
        return UsuarioPermiso.objects.filter(usuario=user, permiso__nombre=required_permission).exists()

class IsRoleOrPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        required_role = getattr(view, 'required_role', None)
        required_permission = getattr(view, 'required_permission', None)

        user = request.user
        if not user.is_authenticated:
            return False

        if required_role and UsuarioRol.objects.filter(usuario=user, rol__nombre=required_role).exists():
            return True
        
        if required_permission and UsuarioPermiso.objects.filter(usuario=user, permiso__nombre=required_permission).exists():
            return True
        
        return False
