import axios from 'axios';
import API_URL from '../utils/constants';

const chatbotService = {
  /**
   * Enviar mensaje al chatbot
   */
  sendMessage: async (message, sessionId = null, token) => {
    const response = await axios.post(
      `${API_URL}/chatbot/message/`,
      {
        message,
        session_id: sessionId
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Obtener historial de una sesión
   */
  getHistory: async (sessionId, token) => {
    const response = await axios.get(
      `${API_URL}/chatbot/history/?session_id=${sessionId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Listar todas las sesiones del usuario
   */
  getSessions: async (token) => {
    const response = await axios.get(
      `${API_URL}/chatbot/sessions/`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Eliminar una sesión
   */
  deleteSession: async (sessionId, token) => {
    const response = await axios.delete(
      `${API_URL}/chatbot/sessions/delete/?session_id=${sessionId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return response.data;
  }
};

export default chatbotService;
