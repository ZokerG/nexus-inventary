import axios from 'axios';
import API_URL from '../utils/constants';

const empresaService = {
  /**
   * Obtener todas las empresas
   */
  getAll: async (token) => {
    const response = await axios.get(`${API_URL}/empresas/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  },

  /**
   * Obtener una empresa por NIT
   */
  getOne: async (nit, token) => {
    const response = await axios.get(`${API_URL}/empresas/${nit}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  },

  /**
   * Crear una nueva empresa
   */
  create: async (empresaData, token) => {
    const response = await axios.post(`${API_URL}/empresas/`, empresaData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  /**
   * Actualizar una empresa existente
   */
  update: async (nit, empresaData, token) => {
    const response = await axios.put(`${API_URL}/empresas/${nit}/`, empresaData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  /**
   * Eliminar una empresa
   */
  delete: async (nit, token) => {
    const response = await axios.delete(`${API_URL}/empresas/${nit}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  }
};

export default empresaService;
