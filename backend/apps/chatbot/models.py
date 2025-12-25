from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatSession(models.Model):
    """Sesión de chat por usuario con caché de Gemini"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    gemini_cache_name = models.CharField(max_length=255, null=True, blank=True)
    cache_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Sesión de Chat'
        verbose_name_plural = 'Sesiones de Chat'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat {self.id} - {self.user.email}"


class ChatMessage(models.Model):
    """Mensajes individuales en una sesión"""
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('model', 'Modelo'),
        ('tool', 'Herramienta'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    tool_calls = models.JSONField(null=True, blank=True)  # Registro de function calls ejecutados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mensaje de Chat'
        verbose_name_plural = 'Mensajes de Chat'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
