from rest_framework import serializers
from .orm_models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer for Empresa model"""
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Empresa
        fields = ('nit', 'nombre', 'direccion', 'telefono', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def validate_nit(self, value):
        """Validar formato NIT"""
        if not value.strip():
            raise serializers.ValidationError("El NIT no puede estar vacío")
        return value.strip()
    
    def validate_telefono(self, value):
        """Validar que el teléfono solo contenga números y caracteres válidos"""
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números")
        return value
