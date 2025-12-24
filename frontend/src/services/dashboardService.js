import axios from 'axios';
import API_URL from '../utils/constants';

const dashboardService = {
  /**
   * Obtener estadísticas del dashboard
   */
  getStats: async (token) => {
    const response = await axios.get(`${API_URL}/auth/dashboard/stats/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  }
};

export default dashboardService;
