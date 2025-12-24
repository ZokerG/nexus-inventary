from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'role', 'first_name', 'last_name')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        role = validated_data.pop('role', User.Role.EXTERNO)
        password = validated_data.pop('password')
        
        # Crear usuario sin password primero
        user = User(**validated_data)
        user.role = role
        user.set_password(password)  # Encriptar password
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user profile details"""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined', 'role')
