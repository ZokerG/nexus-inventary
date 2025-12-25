from django.urls import path
from .views import (
    ChatMessageAPIView,
    ChatHistoryAPIView,
    ChatSessionListAPIView,
    ChatSessionDeleteAPIView
)

urlpatterns = [
    path('message/', ChatMessageAPIView.as_view(), name='chat-message'),
    path('history/', ChatHistoryAPIView.as_view(), name='chat-history'),
    path('sessions/', ChatSessionListAPIView.as_view(), name='chat-sessions'),
    path('sessions/delete/', ChatSessionDeleteAPIView.as_view(), name='chat-session-delete'),
]
