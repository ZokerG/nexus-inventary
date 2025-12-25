from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatMessageInputSerializer,
    ChatMessageResponseSerializer,
    ChatSessionSerializer
)
from .services.gemini_service import GeminiService
from .tools.registry import get_all_tools


@extend_schema(tags=['Chatbot'])
class ChatMessageAPIView(APIView):
    """Endpoint para enviar mensajes al chatbot"""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Enviar mensaje al chatbot",
        description="Envía un mensaje al chatbot y recibe una respuesta inteligente con function calling automático",
        request=ChatMessageInputSerializer,
        responses={200: ChatMessageResponseSerializer}
    )
    def post(self, request):
        serializer = ChatMessageInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Datos inválidos", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id')
        
        # Obtener o crear sesión
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=user)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(user=user)
        else:
            # Buscar sesión activa o crear nueva
            session = ChatSession.objects.filter(user=user, is_active=True).first()
            if not session:
                session = ChatSession.objects.create(user=user)
        
        # Guardar mensaje del usuario
        user_message = ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )
        
        # Obtener herramientas disponibles
        tools = get_all_tools()
        
        # Enviar mensaje a Gemini
        gemini_service = GeminiService()
        
        try:
            # Preparar mensaje con contexto del usuario
            user_context_message = f"{message}\n\n[user_email: {user.email}]"
            
            result = gemini_service.send_message(
                session=session,
                user=user,
                message=user_context_message,
                tools=tools
            )
            
            # Guardar respuesta del modelo
            bot_message = ChatMessage.objects.create(
                session=session,
                role='model',
                content=result['text'],
                tool_calls=result.get('tool_calls')
            )
            
            # Actualizar timestamp de sesión
            session.save()
            
            return Response({
                "session_id": session.id,
                "message": result['text'],
                "tool_calls": result.get('tool_calls'),
                "created_at": bot_message.created_at
            })
        
        except Exception as e:
            return Response(
                {"error": "Error al procesar mensaje", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Chatbot'])
class ChatHistoryAPIView(APIView):
    """Endpoint para obtener el historial de una sesión"""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Obtener historial de chat",
        description="Obtiene el historial completo de mensajes de una sesión de chat",
        parameters=[
            OpenApiParameter(
                name='session_id',
                description='ID de la sesión de chat',
                required=True,
                type=OpenApiTypes.INT
            )
        ],
        responses={200: ChatSessionSerializer}
    )
    def get(self, request):
        session_id = request.query_params.get('session_id')
        
        if not session_id:
            return Response(
                {"error": "session_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Sesión no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=['Chatbot'])
class ChatSessionListAPIView(APIView):
    """Endpoint para listar todas las sesiones del usuario"""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar sesiones de chat",
        description="Obtiene todas las sesiones de chat del usuario actual",
        responses={200: ChatSessionSerializer(many=True)}
    )
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Chatbot'])
class ChatSessionDeleteAPIView(APIView):
    """Endpoint para eliminar una sesión de chat"""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Eliminar sesión de chat",
        description="Elimina una sesión de chat y todos sus mensajes",
        parameters=[
            OpenApiParameter(
                name='session_id',
                description='ID de la sesión a eliminar',
                required=True,
                type=OpenApiTypes.INT
            )
        ]
    )
    def delete(self, request):
        session_id = request.query_params.get('session_id')
        
        if not session_id:
            return Response(
                {"error": "session_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            session.delete()
            return Response({"message": "Sesión eliminada exitosamente"})
        
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Sesión no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
