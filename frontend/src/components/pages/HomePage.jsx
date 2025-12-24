import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Button from '../atoms/Button';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Bienvenido al Sistema de Inventario</h1>
        <p className="welcome-message">
          Hola, <strong>{user?.first_name} {user?.last_name}</strong>
        </p>
        <p className="role-badge">
          Rol: <span className={`badge badge-${user?.role?.toLowerCase()}`}>
            {user?.role === 'ADMIN' ? 'Administrador' : 'Usuario Externo'}
          </span>
        </p>

        <div className="actions">
          <Button onClick={() => navigate('/empresas')} variant="primary">
            Ver Empresas
          </Button>
          {user?.role === 'ADMIN' && (
            <>
              <Button onClick={() => navigate('/productos')} variant="primary">
                Ver Productos
              </Button>
              <Button onClick={() => navigate('/inventario')} variant="primary">
                Ver Inventario
              </Button>
            </>
          )}
          <Button onClick={handleLogout} variant="danger">
            Cerrar Sesión
          </Button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
