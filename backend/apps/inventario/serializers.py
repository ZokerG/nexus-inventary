from rest_framework import serializers
from .models import Inventario


class InventarioSerializer(serializers.ModelSerializer):
    """Serializer for Inventario"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_codigo = serializers.CharField(source='producto.codigo', read_only=True)
    
    class Meta:
        model = Inventario
        fields = ('id', 'empresa', 'empresa_nombre', 'producto', 'producto_nombre', 
                  'producto_codigo', 'cantidad', 'fecha_registro', 'updated_at')
        read_only_fields = ('fecha_registro', 'updated_at')
    
    def validate_cantidad(self, value):
        """Validar que la cantidad no sea negativa"""
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value
