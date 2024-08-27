from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'roles', views.RolViewSet)
router.register(r'permisos', views.PermisoViewSet)
router.register(r'usuario-roles', views.UsuarioRolViewSet)
router.register(r'rol-permisos', views.RolPermisoViewSet)
router.register(r'usuario-permisos', views.UsuarioPermisoViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
