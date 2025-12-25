import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMessageCircle, FiX, FiSend, FiMinimize2 } from 'react-icons/fi';
import { BsRobot } from 'react-icons/bs';
import { useAuth } from '../../../context/AuthContext';
import chatbotService from '../../../services/chatbotService';
import './ChatBot.css';

const ChatBot = () => {
  const { tokens } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      // Mensaje de bienvenida
      setMessages([
        {
          id: Date.now(),
          role: 'model',
          content: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?',
          timestamp: new Date().toISOString()
        }
      ]);
    }
  }, [isOpen, messages.length]);

  const handleSendMessage = useCallback(async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const token = tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
      const response = await chatbotService.sendMessage(
        inputMessage,
        sessionId,
        token
      );

      const botMessage = {
        id: Date.now() + 1,
        role: 'model',
        content: response.message,
        timestamp: response.created_at,
        tool_calls: response.tool_calls
      };

      setMessages(prev => [...prev, botMessage]);
      
      if (!sessionId) {
        setSessionId(response.session_id);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'model',
        content: '❌ Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  }, [inputMessage, isLoading, sessionId, tokens]);

  const handleNewChat = useCallback(() => {
    setMessages([
      {
        id: Date.now(),
        role: 'model',
        content: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?',
        timestamp: new Date().toISOString()
      }
    ]);
    setSessionId(null);
  }, []);

  return (
    <>
      {/* Botón flotante */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="chatbot-fab"
          >
            <div className="chatbot-fab-gradient">
              <BsRobot className="chatbot-fab-icon" />
            </div>
            <span className="chatbot-status-badge">En línea</span>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Modal del chat */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="chatbot-modal"
          >
            {/* Header */}
            <div className="chatbot-header">
              <div className="chatbot-header-content">
                <div className="chatbot-avatar">
                  <BsRobot />
                </div>
                <div className="chatbot-header-info">
                  <h3>Asistente Virtual</h3>
                  <span className="chatbot-status">
                    <span className="status-dot"></span>
                    En línea
                  </span>
                </div>
              </div>
              <div className="chatbot-header-actions">
                <button
                  onClick={handleNewChat}
                  className="chatbot-icon-btn"
                  title="Nueva conversación"
                >
                  <FiMinimize2 />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="chatbot-icon-btn"
                  title="Cerrar"
                >
                  <FiX />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="chatbot-messages">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`chatbot-message ${message.role === 'user' ? 'user-message' : 'bot-message'}`}
                >
                  {message.role === 'model' && (
                    <div className="message-avatar">
                      <BsRobot />
                    </div>
                  )}
                  <div className="message-bubble">
                    <div className="message-content">{message.content}</div>
                    <div className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString('es-ES', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                </motion.div>
              ))}
              
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="chatbot-message bot-message"
                >
                  <div className="message-avatar">
                    <BsRobot />
                  </div>
                  <div className="message-bubble">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSendMessage} className="chatbot-input-container">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Escribe tu mensaje..."
                className="chatbot-input"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isLoading}
                className="chatbot-send-btn"
              >
                <FiSend />
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatBot;
