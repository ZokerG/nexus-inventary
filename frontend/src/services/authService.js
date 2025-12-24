import axios from 'axios';
import API_URL from '../utils/constants';

const authService = {
  /**
   * Login de usuario
   */
  login: async (email, password) => {
    const response = await axios.post(`${API_URL}/auth/login/`, {
      email,
      password
    });
    return response.data;
  },

  /**
   * Registro de usuario (público - solo EXTERNO)
   */
  register: async (userData) => {
    const response = await axios.post(`${API_URL}/auth/register/`, {
      ...userData,
      role: 'EXTERNO' // Por defecto siempre EXTERNO en registro público
    });
    return response.data;
  },

  /**
   * Registro de admin (solo para admins autenticados)
   */
  registerAdmin: async (userData, token) => {
    const response = await axios.post(`${API_URL}/auth/register/`, 
      {
        ...userData,
        role: 'ADMIN'
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
   * Obtener perfil del usuario autenticado
   */
  getProfile: async (token) => {
    const response = await axios.get(`${API_URL}/auth/profile/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  },

  /**
   * Refrescar token
   */
  refreshToken: async (refreshToken) => {
    const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
      refresh: refreshToken
    });
    return response.data;
  }
};

export default authService;
