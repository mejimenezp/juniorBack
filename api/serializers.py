from rest_framework import serializers
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, UsuarioPermiso
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    roles = RolSerializer(many=True, read_only=True, source='roles.rol')
    permisos = PermisoSerializer(many=True, read_only=True, source='permisos.permiso')

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email','nombre','password' ,'is_active', 'is_staff', 'roles', 'permisos']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def get_roles(self, obj):
        return RolSerializer(obj.roles.all(), many=True).data

    def get_permisos(self, obj):
        return PermisoSerializer(obj.permisos.all(), many=True).data

class UsuarioRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRol
        fields = ['usuario', 'rol']

class RolPermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPermiso
        fields = ['rol', 'permiso']

class UsuarioPermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPermiso
        fields = ['usuario', 'permiso_id']
    def update(self, instance, validated_data):
       
        permisos = validated_data.get('permiso_id', instance.permiso)
        instance.permiso.set(permisos)  
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        roles = [rol.rol.nombre for rol in user.roles.all()]
        
        permissions = [perm.permiso.nombre for perm in user.permisos.all()]

        data.update({
            'username': user.username,
            'roles': roles,
            'permissions': permissions
        })
        return data


