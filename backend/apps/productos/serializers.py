from rest_framework import serializers
from .orm_models import Producto, PrecioMoneda


class PrecioMonedaSerializer(serializers.ModelSerializer):
    """Serializer for PrecioMoneda"""
    class Meta:
        model = PrecioMoneda
        fields = ('id', 'moneda', 'precio')
    
    def validate_precio(self, value):
        """Validar que el precio sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return value


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer for Producto with nested prices"""
    precios = PrecioMonedaSerializer(many=True, required=False)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Producto
        fields = ('codigo', 'nombre', 'caracteristicas', 'empresa', 'empresa_nombre', 
                  'precios', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """Crear producto con precios"""
        precios_data = validated_data.pop('precios', [])
        producto = Producto.objects.create(**validated_data)
        
        for precio_data in precios_data:
            PrecioMoneda.objects.create(producto=producto, **precio_data)
        
        return producto
    
    def update(self, instance, validated_data):
        """Actualizar producto y sus precios"""
        precios_data = validated_data.pop('precios', None)
        
        # Actualizar campos del producto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar precios si se proporcionaron
        if precios_data is not None:
            # Eliminar precios existentes
            instance.precios.all().delete()
            # Crear nuevos precios
            for precio_data in precios_data:
                PrecioMoneda.objects.create(producto=instance, **precio_data)
        
        return instance
