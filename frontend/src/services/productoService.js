import axios from 'axios';
import API_URL from '../utils/constants';

const productoService = {
  /**
   * Obtener todos los productos
   */
  getAll: async (token) => {
    const response = await axios.get(`${API_URL}/productos/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  },

  /**
   * Obtener un producto por código
   */
  getOne: async (codigo, token) => {
    const response = await axios.get(`${API_URL}/productos/${codigo}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  },

  /**
   * Crear un nuevo producto
   */
  create: async (productoData, token) => {
    const response = await axios.post(`${API_URL}/productos/`, productoData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  /**
   * Actualizar un producto existente
   */
  update: async (codigo, productoData, token) => {
    const response = await axios.put(`${API_URL}/productos/${codigo}/`, productoData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  /**
   * Eliminar un producto
   */
  delete: async (codigo, token) => {
    const response = await axios.delete(`${API_URL}/productos/${codigo}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  }
};

export default productoService;
