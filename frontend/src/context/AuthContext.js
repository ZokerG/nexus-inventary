import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';

const AuthContext = createContext();
console.log('AuthContext initialized');

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);

  // Cargar datos del usuario desde localStorage al iniciar
  useEffect(() => {
    const storedTokens = localStorage.getItem('tokens');
    const storedUser = localStorage.getItem('user');

    if (storedTokens && storedUser) {
      setTokens(JSON.parse(storedTokens));
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  /**
   * Login
   */
  const login = async (email, password) => {
    try {
      const data = await authService.login(email, password);
      
      setUser(data.user);
      setTokens(data.tokens);
      
      // Guardar en localStorage
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('tokens', JSON.stringify(data.tokens));
      
      return { success: true, user: data.user };
    } catch (error) {
      const message = error.response?.data?.error || 'Error al iniciar sesión';
      return { success: false, error: message };
    }
  };

  /**
   * Registro público (EXTERNO)
   */
  const register = async (userData) => {
    try {
      const data = await authService.register(userData);
      
      setUser(data.user);
      setTokens(data.tokens);
      
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('tokens', JSON.stringify(data.tokens));
      
      return { success: true, user: data.user };
    } catch (error) {
      const message = error.response?.data?.email?.[0] || 
                      error.response?.data?.username?.[0] ||
                      'Error al registrarse';
      return { success: false, error: message };
    }
  };

  /**
   * Logout
   */
  const logout = () => {
    setUser(null);
    setTokens(null);
    localStorage.removeItem('user');
    localStorage.removeItem('tokens');
  };

  /**
   * Verificar si es admin
   */
  const isAdmin = () => {
    return user?.role === 'ADMIN';
  };

  /**
   * Verificar si está autenticado
   */
  const isAuthenticated = () => {
    return !!user && !!tokens;
  };

  const value = {
    user,
    tokens,
    loading,
    login,
    register,
    logout,
    isAdmin,
    isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
