from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import UserSerializer, LoginSerializer, UserDetailSerializer
from .permissions import IsAdminUser

User = get_user_model()


@extend_schema(tags=['Autenticación'])
class RegisterView(generics.CreateAPIView):
    """
    Registro de nuevos usuarios
    
    Solo administradores pueden crear otros administradores.
    Usuarios externos pueden auto-registrarse.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Registro de usuario",
        description="Crear una nueva cuenta de usuario. Solo admins pueden crear usuarios con rol ADMIN.",
        examples=[
            OpenApiExample(
                'Usuario Externo',
                value={
                    'email': 'usuario@example.com',
                    'username': 'usuario',
                    'password': 'SecurePass123!',
                    'role': 'EXTERNO',
                    'first_name': 'Juan',
                    'last_name': 'Pérez'
                }
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        # Solo admins pueden crear otros admins
        if request.data.get('role') == User.Role.ADMIN:
            if not request.user.is_authenticated or not request.user.is_admin:
                return Response(
                    {'error': 'Solo administradores pueden crear usuarios administradores'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Autenticación'])
class LoginView(APIView):
    """
    Inicio de sesión con email y contraseña
    
    Retorna tokens JWT (access y refresh)
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    @extend_schema(
        summary="Iniciar sesión",
        description="Autenticar usuario con email y contraseña. Retorna tokens JWT.",
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                'Login Ejemplo',
                value={
                    'email': 'admin@example.com',
                    'password': 'SecurePass123!'
                }
            ),
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Autenticar directamente con email (USERNAME_FIELD)
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


@extend_schema(tags=['Autenticación'])
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Obtener o actualizar perfil del usuario autenticado
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Obtener perfil",
        description="Obtener información del usuario autenticado"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar perfil",
        description="Actualizar información del usuario autenticado"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar perfil parcial",
        description="Actualizar parcialmente información del usuario autenticado"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user
