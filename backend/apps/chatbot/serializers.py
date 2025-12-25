from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'tool_calls', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_active', 'messages']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ChatMessageInputSerializer(serializers.Serializer):
    """Serializer para input del usuario"""
    message = serializers.CharField(required=True)
    session_id = serializers.UUIDField(required=False, allow_null=True)


class ChatMessageResponseSerializer(serializers.Serializer):
    """Serializer para respuesta del chatbot"""
    session_id = serializers.IntegerField()
    message = serializers.CharField()
    tool_calls = serializers.JSONField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
