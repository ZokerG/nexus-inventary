import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const inventarioService = {
  getAll: async (token) => {
    const response = await axios.get(`${API_URL}/inventario/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  },

  getById: async (id, token) => {
    const response = await axios.get(`${API_URL}/inventario/${id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  },

  create: async (data, token) => {
    const response = await axios.post(`${API_URL}/inventario/`, data, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  update: async (id, data, token) => {
    const response = await axios.put(`${API_URL}/inventario/${id}/`, data, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  delete: async (id, token) => {
    const response = await axios.delete(`${API_URL}/inventario/${id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  },

  exportPDF: async (empresaNit, token) => {
    const url = empresaNit 
      ? `${API_URL}/inventario/export_pdf/?empresa=${empresaNit}`
      : `${API_URL}/inventario/export_pdf/`;
    
    const response = await axios.get(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      responseType: 'blob'
    });
    
    // Crear URL de descarga
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `inventario_${empresaNit || 'completo'}_${Date.now()}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(downloadUrl);
    
    return response.data;
  },

  sendEmail: async (email, empresaNit, token) => {
    const data = {
      email,
      ...(empresaNit && { empresa: empresaNit })
    };
    
    const response = await axios.post(`${API_URL}/inventario/send_email/`, data, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  }
};

export default inventarioService;
