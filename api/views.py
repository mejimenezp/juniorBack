from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, UsuarioPermiso
from .serializers import UsuarioSerializer, RolSerializer, PermisoSerializer, UsuarioRolSerializer, RolPermisoSerializer, UsuarioPermisoSerializer
from .permissions import IsRoleOrPermission,IsUserWithRole
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UsuarioViewSet(viewsets.ModelViewSet):    
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsRoleOrPermission]
    required_role = 'Administrador'
    required_permission = 'Leer Datos'

    def perform_update(self, serializer):
        user = self.request.user
        if serializer.instance.is_staff and user.is_authenticated and not user.roles.filter(nombre='Administrador').exists():
            raise PermissionDenied("No tienes permiso para cambiar este usuario.")
        super().perform_update(serializer)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsUserWithRole]
    required_role = 'Administrador'


class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer
    permission_classes = [IsAuthenticated, IsUserWithRole]
    required_role = 'Administrador'


class UsuarioRolViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRol.objects.all()
    serializer_class = UsuarioRolSerializer
    permission_classes = [IsAuthenticated, IsRoleOrPermission]
    required_role = 'Ingeniero', 'Administrador'
    required_permission = 'Administrar Usuarios'

    def update(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('pk')
        rol_id = request.data.get('rol_id')

        
        usuario_rol = UsuarioRol.objects.filter(usuario_id=usuario_id, rol_id=rol_id).first()
        if not usuario_rol:
           
            usuario_rol = UsuarioRol.objects.create(usuario_id=usuario_id, rol_id=rol_id)
        else:
           
            usuario_rol.rol_id = rol_id
            usuario_rol.save()
        
       
        serializer = UsuarioRolSerializer(usuario_rol)
        return Response(serializer.data)



class RolPermisoViewSet(viewsets.ModelViewSet):
    queryset = RolPermiso.objects.all()
    serializer_class = RolPermisoSerializer
    permission_classes = [IsAuthenticated, IsUserWithRole]
    required_role = 'Administrador'

class UsuarioPermisoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPermiso.objects.all()
    serializer_class = UsuarioPermisoSerializer
    permission_classes = [IsAuthenticated, IsUserWithRole]
    required_role = 'Administrador'

    def update(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('pk')
        permiso_id = request.data.get('permiso_id')

        
        usuario_permiso = UsuarioPermiso.objects.filter(usuario_id=usuario_id, permiso_id=permiso_id).first()
        if not usuario_permiso:
            
            usuario_permiso = UsuarioPermiso.objects.create(usuario_id=usuario_id, permiso_id=permiso_id)
        else:
            
            usuario_permiso.permiso_id = permiso_id
            usuario_permiso.save()
        
        
        serializer = UsuarioPermisoSerializer(usuario_permiso)
        return Response(serializer.data)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
